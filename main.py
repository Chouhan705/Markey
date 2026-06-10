import threading
import os
import sys
import keyboard
from pystray import Icon, Menu, MenuItem
from PIL import Image
from ocr_engine import run_ocr
from gui import MarkeyWindow, MarkeySetupWindow
import config_manager

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def trigger_markey():
    print("\n[MARKEY] Triggered...")
    try:
        captured_text = run_ocr()
        if not captured_text or captured_text.startswith("Error:"):
            print(f"[MARKEY] OCR Failed or Empty: {captured_text}")
            return

        def launch_gui():
            app = MarkeyWindow(captured_text, lambda t, c, tp: format_to_markdown(t, c, tp))
            app.show()

        ui_thread = threading.Thread(target=launch_gui)
        ui_thread.start()
        
    except Exception as e:
        print(f"Error in execution thread: {e}")

from formatter import format_to_markdown

def launch_settings_editor():
    """ Opens the template editor from the tray without freezing the background service """
    def run_editor():
        editor = MarkeySetupWindow(is_welcome_mode=False)
        editor.show()
    
    editor_thread = threading.Thread(target=run_editor)
    editor_thread.start()

def on_quit(icon, item):
    icon.stop()
    os._exit(0)

def setup_tray():
    icon_path = resource_path("logo.png")
    try:
        img = Image.open(icon_path)
    except Exception:
        img = Image.new('RGB', (64, 64), color=(41, 128, 185))
    
    # Updated Tray Layout to include our Settings panel trigger
    menu = Menu(
        MenuItem("Markey is Running", lambda: None, enabled=False), 
        MenuItem("Edit Templates...", launch_settings_editor),
        MenuItem("Exit", on_quit)
    )
    icon = Icon("Markey", img, "Markey", menu)
    icon.run()

if __name__ == "__main__":
    print("=== Markey Initializing ===")
    
    # Step 1 & 2: Handle First Run Onboarding interception safely on core main-thread loop
    if config_manager.is_first_run():
        print("[MARKEY] First run detected. Laundering setup onboarding wizard...")
        welcome_wizard = MarkeySetupWindow(is_welcome_mode=True)
        welcome_wizard.show()
    
    # Step 3: Register global hooks and start background runtime service environment
    keyboard.add_hotkey('ctrl+alt+m', trigger_markey, suppress=True)
    
    setup_tray()