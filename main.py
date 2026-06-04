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

def create_image():
    """Creates a simple 'M' icon for the system tray if you don't have a .png file"""
    width, height = 64, 64
    image = Image.new('RGB', (width, height), color=(41, 128, 185)) # Blue background
    dc = ImageDraw.Draw(image)
    # Draw a simple white 'M'
    dc.text((20, 15), "M", fill=(255, 255, 255), font_size=40)
    return image

def on_quit(icon, item):
    icon.stop()
    os._exit(0) # Force exit the whole script

def setup_tray():
    # Define the menu
    menu = Menu(
        MenuItem("Markey is Running", lambda: None, enabled=False),
        MenuItem("Exit", on_quit)
    )
    
    # Create the icon
    # Note: You can replace create_image() with Image.open("your_logo.png") later
    icon = Icon("Markey", create_image(), "Markey - Clipboard to Markdown", menu)
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