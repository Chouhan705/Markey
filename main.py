import threading
import os
import sys
import keyboard
from pystray import Icon, Menu, MenuItem
from PIL import Image

# Core components
from ocr_engine import run_ocr
from gui import MarkeyWindow, MarkeySetupWindow
from formatter import format_to_markdown
from notification_manager import show_toast
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
        
        # Error validation checks with Toast Alerts
        if not captured_text:
            show_toast("Markey Error", "No clear text could be read from the image.")
            return
            
        if captured_text.startswith("Error:"):
            # Strip baseline string prefix out for clean user display
            err_msg = captured_text.replace("Error:", "").strip()
            show_toast("Markey Notification", err_msg)
            return

        # Success notification!
        show_toast("Markey Active", "Screenshot parsed successfully! Select layout.")

        def launch_gui():
            app = MarkeyWindow(captured_text, lambda t, c, tp: format_to_markdown(t, c, tp))
            app.show()

        ui_thread = threading.Thread(target=launch_gui)
        ui_thread.start()
        
    except Exception as e:
        print(f"Error in execution thread: {e}")

def launch_settings_editor():
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
    
    keyboard.add_hotkey('ctrl+alt+m', trigger_markey, suppress=True)
    
    setup_tray()