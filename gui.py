import tkinter as tk
import os
import sys
from config_manager import load_config, save_config
from PIL import Image, ImageTk 

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
        
        try:
            icon_path = resource_path("logo.png")
            if os.path.exists(icon_path):
                self.root.iconphoto(False, tk.PhotoImage(file=icon_path))
        except Exception: pass

        self.extracted_text = extracted_text
        self.callback = callback
        
        # Geometry setup
        self.root.attributes('-topmost', True)
        self.root.geometry("300x250")
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"+{int(sw/2-150)}+{int(sh/2-125)}")

        tk.Label(self.root, text="Format for Markey:", font=("Arial", 10, "bold")).pack(pady=10)
        
        # Load active template labels dynamically from config
        config = load_config()
        t1 = config["templates"]["1"].split("\n")[0].replace("#", "").strip()
        t2 = config["templates"]["2"].split("\n")[0].replace("#", "").strip()
        t3 = config["templates"]["3"].split("\n")[0].replace("#", "").strip()

        tk.Button(self.root, text=f"[1] {t1}", width=25, command=lambda: self.submit("1")).pack(pady=2)
        tk.Button(self.root, text=f"[2] {t2}", width=25, command=lambda: self.submit("2")).pack(pady=2)
        tk.Button(self.root, text=f"[3] {t3}", width=25, command=lambda: self.submit("3")).pack(pady=2)
        
        tk.Label(self.root, text="Custom Topic:").pack(pady=5)
        self.custom_entry = tk.Entry(self.root, width=30)
        self.custom_entry.pack(pady=5)
        self.custom_entry.bind("<Return>", lambda e: self.submit("custom"))
        
        self.root.bind("1", lambda e: self.handle_quick_key("1"))
        self.root.bind("2", lambda e: self.handle_quick_key("2"))
        self.root.bind("3", lambda e: self.handle_quick_key("3"))

        self.root.lift()
        self.root.focus_force()
        self.custom_entry.focus_set()
        self.root.after(100, lambda: self.root.focus_force())

    def handle_quick_key(self, choice):
        if self.root.focus_get() == self.custom_entry:
            return
        self.submit(choice)

    def submit(self, choice):
        topic = self.custom_entry.get()
        self.root.destroy()
        self.callback(self.extracted_text, choice, topic)

    def show(self):
        self.root.mainloop()


class MarkeySetupWindow:
    """ Handling both the Welcome greeting and runtime customization settings """
    def __init__(self, is_welcome_mode=False):
        self.root = tk.Tk()
        self.root.title("Markey Setup Wizard" if is_welcome_mode else "Edit Templates")
        
        try:
            icon_path = resource_path("logo.png")
            if os.path.exists(icon_path):
                self.root.iconphoto(False, tk.PhotoImage(file=icon_path))
        except Exception: pass

        self.root.attributes('-topmost', True)
        self.root.geometry("450x420")
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"+{int(sw/2-225)}+{int(sh/2-210)}")
        original_img = Image.open("Logo.png")
        resized_img = original_img.resize((100, 100), Image.Resampling.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(resized_img)

        if is_welcome_mode:
            tk.Label(self.root, image=self.logo_img).pack(pady=(20, 10)) 

            tk.Label(self.root, text="Welcome to Markey!", font=("Arial", 14, "bold"), fg="#2980b9").pack(pady=10)
            tk.Label(self.root, text="Let's customize your quick-key templates. Use {text} where\nyou want your screenshot text to be injected.", font=("Arial", 9, "italic")).pack(pady=5)
        else:
            tk.Label(self.root, text="Modify Prompt Templates", font=("Arial", 12, "bold")).pack(pady=10)

        config = load_config()
        
       # Field 1
        tk.Label(self.root, text="Template [1] Layout:", font=("Arial", 9, "bold")).pack(anchor="w", padx=25)
        self.t1_text = tk.Text(self.root, height=3, width=50)
        self.t1_text.pack(pady=2)
        self.t1_text.insert("1.0", config["templates"]["1"])

        # Field 2
        tk.Label(self.root, text="Template [2] Layout:", font=("Arial", 9, "bold")).pack(anchor="w", padx=25)
        self.t2_text = tk.Text(self.root, height=3, width=50)
        self.t2_text.pack(pady=2)
        self.t2_text.insert("1.0", config["templates"]["2"])

        # Field 3
        tk.Label(self.root, text="Template [3] Layout:", font=("Arial", 9, "bold")).pack(anchor="w", padx=25)
        self.t3_text = tk.Text(self.root, height=3, width=50)
        self.t3_text.pack(pady=2)
        self.t3_text.insert("1.0", config["templates"]["3"])
        tk.Button(self.root, text="Save Configuration", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), width=25, command=self.save_settings).pack(pady=15)

    def save_settings(self):
        new_config = {
            "templates": {
                "1": self.t1_text.get("1.0", "end-1c").strip(),
                "2": self.t2_text.get("1.0", "end-1c").strip(),
                "3": self.t3_text.get("1.0", "end-1c").strip(),
            }
        }
        save_config(new_config)
        self.root.destroy()

    def show(self):
        self.root.lift()
        self.root.focus_force()
        self.root.mainloop()