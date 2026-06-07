import threading
import os
import sys
import keyboard
from pystray import Icon, Menu, MenuItem
from PIL import Image
from ocr_engine import run_ocr
from gui import MarkeyWindow
from formatter import format_to_markdown

def trigger_markey():
    print("\n[MARKER] Triggered...")
    try:
        captured_text = run_ocr()
        if not captured_text or "Error:" in captured_text:
            return

        def launch_gui():
            app = MarkeyWindow(captured_text, lambda t, c, tp: format_to_markdown(t, c, tp))
            app.show()

        threading.Thread(target=launch_gui, daemon=True).start()
    except Exception as e:
        print(f"Error: {e}")

def on_quit(icon, item):
    icon.stop()
    os._exit(0)

def setup_tray():
    try:
        img = Image.open("logo.png")
    except:
        img = Image.new('RGB', (64, 64), color=(41, 128, 185))
    
    menu = Menu(MenuItem("Markey is Running", lambda: None, enabled=False), MenuItem("Exit", on_quit))
    icon = Icon("Markey", img, "Markey", menu)
    icon.run()

if __name__ == "__main__":
    print("=== Markey v1.1.0 Ready ===")
    
    # suppress=True prevents the 'ṁ' symbol by blocking the key from other apps
    keyboard.add_hotkey('ctrl+alt+m', trigger_markey, suppress=True)
    
    setup_tray()