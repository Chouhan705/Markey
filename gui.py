import tkinter as tk
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class MarkeyWindow:
    def __init__(self, extracted_text, callback):
        self.root = tk.Tk()
        self.root.title("Markey")
        
        # Icon Logic
        try:
            icon_path = resource_path("logo.png")
            if os.path.exists(icon_path):
                self.root.iconphoto(False, tk.PhotoImage(file=icon_path))
        except: pass

        self.extracted_text = extracted_text
        self.callback = callback
        
        # Focus & Window Settings
        self.root.attributes('-topmost', True)
        self.root.geometry("300x250")
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"+{int(sw/2-150)}+{int(sh/2-125)}")

        tk.Label(self.root, text="Format for Markey:", font=("Arial", 10, "bold")).pack(pady=10)
        
        tk.Button(self.root, text="[1] VS Code Error", width=25, command=lambda: self.submit("1")).pack(pady=2)
        tk.Button(self.root, text="[2] GitHub Discussion", width=25, command=lambda: self.submit("2")).pack(pady=2)
        tk.Button(self.root, text="[3] Website UI", width=25, command=lambda: self.submit("3")).pack(pady=2)
        
        tk.Label(self.root, text="Custom Topic:").pack(pady=5)
        self.custom_entry = tk.Entry(self.root, width=30)
        self.custom_entry.pack(pady=5)
        self.custom_entry.bind("<Return>", lambda e: self.submit("custom"))
        
        # Keybinds
        self.root.bind("1", lambda e: self.submit("1"))
        self.root.bind("2", lambda e: self.submit("2"))
        self.root.bind("3", lambda e: self.submit("3"))

        # Aggressive Focus Logic
        self.root.lift()
        self.root.focus_force()
        self.custom_entry.focus_set()
        # Retry focus after window is fully drawn
        self.root.after(100, lambda: self.root.focus_force())

    def submit(self, choice):
        topic = self.custom_entry.get()
        self.root.destroy()
        self.callback(self.extracted_text, choice, topic)

    def show(self):
        self.root.mainloop()