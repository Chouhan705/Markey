import threading
import os
import sys
import keyboard
from pystray import Icon, Menu, MenuItem
from PIL import Image
import ctypes

# Core structural modules
from ocr_engine import run_ocr
from gui import MarkeyWindow, MarkeySetupWindow
from formatter import format_to_markdown
import config_manager

# Global reference to the system tray icon
tray_icon = None
mutex = None

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def ocr_and_gui_worker():
    """ Dedicated background worker thread preventing COM apartment deadlocks """
    global tray_icon
    try:
        captured_text = run_ocr()
        
        if not captured_text or captured_text.startswith("Error:"):
            print(f"[MARKEY] Extraction halted: {captured_text}")
            if tray_icon:
                # Trigger a secure, native system notification balloon
                tray_icon.notify("No clear text read from the image.", title="Markey Error")
            return

        print(f"[MARKEY] OCR extraction clean. Length: {len(captured_text)} chars.")

        # Success system notification!
        if tray_icon:
            tray_icon.notify("Screenshot parsed successfully! Choose layout.", title="Markey Active")

        # Launch Tkinter layout window
        app = MarkeyWindow(captured_text, lambda t, c, tp: format_to_markdown(t, c, tp))
        app.show()
        
    except Exception as e:
        print(f"[WORKER ERROR] Critical failure: {e}")

def trigger_markey():
    print("\n[MARKEY] Triggered via Hotkey...")
    threading.Thread(target=ocr_and_gui_worker, daemon=True).start()

def launch_settings_editor():
    def run_editor():
        editor = MarkeySetupWindow(is_welcome_mode=False)
        editor.show()
    
    threading.Thread(target=run_editor, daemon=True).start()

def on_quit(icon, item):
    global mutex
    icon.stop()
    # Release the system Mutex handle when cleanly exiting
    if mutex:
        ctypes.windll.kernel32.ReleaseMutex(mutex)
    os._exit(0)

def setup_tray():
    global tray_icon
    icon_path = resource_path("logo.png")
    try:
        img = Image.open(icon_path)
    except Exception:
        img = Image.new('RGB', (64, 64), color=(41, 128, 185))
    
    menu = Menu(
        MenuItem("Markey is Running", lambda: None, enabled=False), 
        MenuItem("Edit Templates...", launch_settings_editor),
        MenuItem("Exit", on_quit)
    )
    
    tray_icon = Icon("Markey", img, "Markey", menu)
    tray_icon.run()

if __name__ == "__main__":
    print("=== Markey Initializing ===")
    
    # --- SINGLE INSTANCE LOCK ENGINE ---
    # Create a system-wide named mutex to guard execution contexts
    ERROR_ALREADY_EXISTS = 183
    mutex_name = "Global\\Markey_SingleInstance_Mutex"
    
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
    last_error = ctypes.windll.kernel32.GetLastError()
    
    if last_error == ERROR_ALREADY_EXISTS:
        print("[MARKEY ALERT] Markey is already running in the background. Exiting duplicate instance safely.")
        sys.exit(0)
    # -----------------------------------

    if config_manager.is_first_run():
        print("[MARKEY] First run detected. Launching setup onboarding wizard...")
        welcome_wizard = MarkeySetupWindow(is_welcome_mode=True)
        welcome_wizard.show()
    
    # Global hook assignment
    keyboard.add_hotkey('ctrl+alt+m', trigger_markey, suppress=True)
    
    setup_tray()