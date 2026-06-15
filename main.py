import threading
import os
import sys
import keyboard
from pystray import Icon, Menu, MenuItem
from PIL import Image

# Core structural modules
from ocr_engine import run_ocr
from gui import MarkeyWindow, MarkeySetupWindow
from formatter import format_to_markdown
import config_manager

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def ocr_and_gui_worker():
    """ 
    Dedicated background worker thread. 
    Isolating this prevents the Windows COM apartment deadlock.
    """
    try:
        captured_text = run_ocr()
        
        if not captured_text or captured_text.startswith("Error:"):
            print(f"[MARKEY] Extraction halted: {captured_text}")
            return

        print(f"[MARKEY] OCR extraction clean. Length: {len(captured_text)} chars.")

        # Safely launch Tkinter window inside this distinct thread instance
        app = MarkeyWindow(captured_text, lambda t, c, tp: format_to_markdown(t, c, tp))
        app.show()
        
    except Exception as e:
        print(f"[WORKER ERROR] Critical failure: {e}")

def trigger_markey():
    print("\n[MARKEY] Triggered via Hotkey...")
    # Fire and forget: offload EVERYTHING immediately to an isolated thread context
    threading.Thread(target=ocr_and_gui_worker, daemon=True).start()

def launch_settings_editor():
    def run_editor():
        editor = MarkeySetupWindow(is_welcome_mode=False)
        editor.show()
    
    threading.Thread(target=run_editor, daemon=True).start()

def on_quit(icon, item):
    icon.stop()
    os._exit(0)

def setup_tray():
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
    icon = Icon("Markey", img, "Markey", menu)
    icon.run()

if __name__ == "__main__":
    print("=== Markey Initializing ===")
    
    if config_manager.is_first_run():
        print("[MARKEY] First run detected. Launching setup onboarding wizard...")
        welcome_wizard = MarkeySetupWindow(is_welcome_mode=True)
        welcome_wizard.show()
    
    # Global hook assignment
    keyboard.add_hotkey('ctrl+alt+m', trigger_markey, suppress=True)
    
    setup_tray()