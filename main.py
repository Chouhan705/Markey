import threading
import sys
import os
from pynput import keyboard
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

# Import your custom modules
from ocr_engine import run_ocr
from gui import MarkeyWindow
from formatter import format_to_markdown

# --- LOGIC ---

def trigger_markey():
    """Triggered by Hotkey"""
    captured_text = run_ocr()
    if "Error:" in captured_text:
        return

    def launch_gui():
        def finalize(text, choice, custom_topic):
            format_to_markdown(text, choice, custom_topic)
        
        app = MarkeyWindow(captured_text, finalize)
        app.show()

    # GUI must run in its own thread to avoid freezing the Tray
    threading.Thread(target=launch_gui, daemon=True).start()

# --- SYSTEM TRAY LOGIC ---


def on_quit(icon, item):
    icon.stop()
    os._exit(0) # Force exit the whole script

def setup_tray():
    menu = Menu(
        MenuItem("Markey is Running", lambda: None, enabled=False),
        MenuItem("Exit", on_quit)
    )
    
    # Load your custom pixel art PNG
    try:
        # Get the path to the icon (handles running as script or as EXE)
        icon_path = "logo.png" 
        if not os.path.exists(icon_path):
            # Fallback if the image is missing
            img = Image.new('RGB', (64, 64), color=(41, 128, 185))
        else:
            img = Image.open(icon_path)
    except Exception:
        img = Image.new('RGB', (64, 64), color=(41, 128, 185))

    icon = Icon("Markey", img, "Markey - Clipboard to Markdown", menu)
    icon.run()

# --- HOTKEY LISTENER ---

def start_hotkey_listener():
    HOTKEY = '<ctrl>+<alt>+m'
    with keyboard.GlobalHotKeys({
            HOTKEY: lambda: threading.Thread(target=trigger_markey, daemon=True).start()
    }) as h:
        h.join()

# --- MAIN EXECUTION ---

if __name__ == "__main__":
    # 1. Start the Hotkey Listener in the background (daemon thread)
    listener_thread = threading.Thread(target=start_hotkey_listener, daemon=True)
    listener_thread.start()

    # 2. Start the System Tray Icon in the foreground
    # (This keeps the script alive)
    print("Markey is active in the System Tray.")
    setup_tray()