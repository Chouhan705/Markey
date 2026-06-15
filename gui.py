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
        
        # Geometry setup - Dynamic Cursor Centering Math
        self.root.attributes('-topmost', True)
        self.root.geometry("300x250")
        
        # Pull active mouse cursor coordinates directly to center window on current screen focus
        try:
            cursor_x = self.root.winfo_pointerx()
            cursor_y = self.root.winfo_pointery()
            self.root.geometry(f"+{int(cursor_x - 150)}+{int(cursor_y - 125)}")
        except Exception:
            sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
            self.root.geometry(f"+{int(sw/2-150)}+{int(sh/2-125)}")

        # Application Custom Branded Design Parameters
        self.root.configure(bg="#1c2d5a")  # Deep Logo Blue Base Background
        
        tk.Label(self.root, text="Format for Markey:", font=("Arial", 11, "bold"), fg="#ffffff", bg="#1c2d5a").pack(pady=12)
        
        config = load_config()
        t1 = config["templates"]["1"].split("\n")[0].replace("#", "").strip()
        t2 = config["templates"]["2"].split("\n")[0].replace("#", "").strip()
        t3 = config["templates"]["3"].split("\n")[0].replace("#", "").strip()

        # Premium interactive button elements using logo color tokens
        btn_style = {"width": 26, "bg": "#2a7d5c", "fg": "#ffffff", "activebackground": "#76e047", "activeforeground": "#1c2d5a", "font": ("Arial", 9, "bold"), "bd": 0, "cursor": "hand2"}
        
        tk.Button(self.root, text=f"[1] {t1}", **btn_style, command=lambda: self.submit("1")).pack(pady=3)
        tk.Button(self.root, text=f"[2] {t2}", **btn_style, command=lambda: self.submit("2")).pack(pady=3)
        tk.Button(self.root, text=f"[3] {t3}", **btn_style, command=lambda: self.submit("3")).pack(pady=3)
        
        tk.Label(self.root, text="Custom Topic:", font=("Arial", 9, "bold"), fg="#ffffff", bg="#1c2d5a").pack(pady=(10, 2))
        self.custom_entry = tk.Entry(self.root, width=32, bg="#ffffff", fg="#1c2d5a", insertbackground="#1c2d5a", font=("Arial", 9))
        self.custom_entry.pack(pady=2)
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
    """ High-Fidelity multi-step wizard tracking onboarding screens dynamically inside one window context """
    def __init__(self, is_welcome_mode=False):
        self.root = tk.Tk()
        self.root.title("Markey Setup Wizard" if is_welcome_mode else "Edit Templates")
        
        try:
            icon_path = resource_path("logo.png")
            if os.path.exists(icon_path):
                self.root.iconphoto(False, tk.PhotoImage(file=icon_path))
        except Exception: pass

        self.root.attributes('-topmost', True)
        self.root.geometry("480x480")
        self.root.configure(bg="#1c2d5a") # Main theme color link
        
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"+{int(sw/2-240)}+{int(sh/2-240)}")

        # Asset Mapping Logic Interception
        try:
            logo_path = resource_path("logo.png")
            original_img = Image.open(logo_path)
            resized_img = original_img.resize((90, 90), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(resized_img)
        except Exception:
            self.logo_img = None

        # State engine tracking 
        # If launched from settings icon tray -> skip straight to customization step panel
        self.current_step = 1 if is_welcome_mode else 3
        
        # Create a persistent frame container to hold dynamic wizard content panels smoothly
        self.content_frame = tk.Frame(self.root, bg="#1c2d5a")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Render baseline state step configuration view index
        self.render_step()

    def clear_current_frame(self):
        """ Completely purges widgets inside content panel frame container before changing states """
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def render_step(self):
        self.clear_current_frame()
        
        # Standard design style mapping parameters
        title_font = ("Arial", 15, "bold")
        body_font = ("Arial", 10)
        btn_next_style = {"bg": "#76e047", "fg": "#1c2d5a", "activebackground": "#2a7d5c", "activeforeground": "#ffffff", "font": ("Arial", 10, "bold"), "bd": 0, "width": 15, "cursor": "hand2"}
        
        # -----------------------------------------------------------------
        # STEP 1: INITIAL GREETING PAGE
        # -----------------------------------------------------------------
        if self.current_step == 1:
            if self.logo_img:
                tk.Label(self.content_frame, image=self.logo_img, bg="#1c2d5a").pack(pady=(30, 10))
            
            tk.Label(self.content_frame, text="Welcome to Markey!", font=title_font, fg="#76e047", bg="#1c2d5a").pack(pady=10)
            
            desc_text = "Your lightweight, privacy-focused clipboard sidekick.\nTransforming images into prompt-ready markdown structures natively."
            tk.Label(self.content_frame, text=desc_text, font=body_font, fg="#ffffff", bg="#1c2d5a", justify="center").pack(pady=15)
            
            tk.Button(self.content_frame, text="Get Started →", **btn_next_style, command=self.next_step).pack(side="bottom", pady=20)

        # -----------------------------------------------------------------
        # STEP 2: APP UTILITY/EXPLANATION INTERACTION OVERVIEW
        # -----------------------------------------------------------------
        elif self.current_step == 2:
            tk.Label(self.content_frame, text="What is Markey?", font=title_font, fg="#76e047", bg="#1c2d5a").pack(pady=(10, 20))
            
            bullet_config = {"anchor": "w", "bg": "#1c2d5a", "fg": "#ffffff", "font": body_font, "justify": "left"}
            
            tk.Label(self.content_frame, text="⚡ Invisible Service: Runs quietly inside your background system tray.", **bullet_config).pack(fill="x", pady=6)
            tk.Label(self.content_frame, text="🎹 Global Trigger: Press [ Ctrl + Alt + M ] instantly after snapping code.", **bullet_config).pack(fill="x", pady=6)
            tk.Label(self.content_frame, text="🔍 Native OCR: Converts layout heights to hierarchical structural markdown.", **bullet_config).pack(fill="x", pady=6)
            tk.Label(self.content_frame, text="🔒 100% Offline: No API keys required. Your screen data never leaves your rig.", **bullet_config).pack(fill="x", pady=6)
            
            tk.Button(self.content_frame, text="Configure Formats →", **btn_next_style, command=self.next_step).pack(side="bottom", pady=20)

        # -----------------------------------------------------------------
        # STEP 3: LIVE CORE CONFIGURATION EDITOR
        # -----------------------------------------------------------------
        elif self.current_step == 3:
            tk.Label(self.content_frame, text="Personalize Prompt Templates", font=("Arial", 13, "bold"), fg="#76e047", bg="#1c2d5a").pack(pady=(0, 5))
            tk.Label(self.content_frame, text="Use {text} placeholder where you want screenshot content to be injected.", font=("Arial", 8, "italic"), fg="#ffffff", bg="#1c2d5a").pack(pady=(0, 10))
            
            config = load_config()
            lbl_style = {"anchor": "w", "bg": "#1c2d5a", "fg": "#ffffff", "font": ("Arial", 9, "bold")}
            txt_style = {"bg": "#ffffff", "fg": "#1c2d5a", "insertbackground": "#1c2d5a", "height": 3, "width": 52, "font": ("Courier New", 9)}

            # Prompt 1
            tk.Label(self.content_frame, text="[1] VS Code / Programming Code Template:", **lbl_style).pack(fill="x", padx=5)
            self.t1_text = tk.Text(self.content_frame, **txt_style)
            self.t1_text.pack(pady=(2, 8))
            self.t1_text.insert("1.0", config["templates"]["1"])

            # Prompt 2
            tk.Label(self.content_frame, text="[2] GitHub / Discussion Template:", **lbl_style).pack(fill="x", padx=5)
            self.t2_text = tk.Text(self.content_frame, **txt_style)
            self.t2_text.pack(pady=(2, 8))
            self.t2_text.insert("1.0", config["templates"]["2"])

            # Prompt 3
            tk.Label(self.content_frame, text="[3] Web UI / Layout Content Template:", **lbl_style).pack(fill="x", padx=5)
            self.t3_text = tk.Text(self.content_frame, **txt_style)
            self.t3_text.pack(pady=(2, 8))
            self.t3_text.insert("1.0", config["templates"]["3"])
            
            tk.Button(self.content_frame, text="Save & Finish →", **btn_next_style, command=self.save_settings).pack(side="bottom", pady=5)

        # -----------------------------------------------------------------
        # STEP 4: FINAL SUCCESS/COMPLETION CARD
        # -----------------------------------------------------------------
        elif self.current_step == 4:
            if self.logo_img:
                tk.Label(self.content_frame, image=self.logo_img, bg="#1c2d5a").pack(pady=(40, 10))
                
            tk.Label(self.content_frame, text="Markey is Fully Armed!", font=title_font, fg="#76e047", bg="#1c2d5a").pack(pady=10)
            tk.Label(self.content_frame, text="The tool is running inside your system taskbar.\nSnip any image area and press [ Ctrl + Alt + M ] anytime.", font=body_font, fg="#ffffff", bg="#1c2d5a", justify="center").pack(pady=10)
            
            tk.Button(self.content_frame, text="Launch Application", **btn_next_style, command=self.root.destroy).pack(side="bottom", pady=30)

    def next_step(self):
        self.current_step += 1
        self.render_step()

    def save_settings(self):
        new_config = {
            "templates": {
                "1": self.t1_text.get("1.0", "end-1c").strip(),
                "2": self.t2_text.get("1.0", "end-1c").strip(),
                "3": self.t3_text.get("1.0", "end-1c").strip(),
            }
        }
        save_config(new_config)
        
        # Route logic tracking: If we edited from system tray icon -> terminate instantly. 
        # If we are in first-run welcome wizard flow -> advance into success screen.
        if self.root.title() == "Edit Templates":
            self.root.destroy()
        else:
            self.next_step()

    def show(self):
        self.root.lift()
        self.root.focus_force()
        self.root.mainloop()