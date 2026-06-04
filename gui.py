import tkinter as tk

class MarkeyWindow:
    def __init__(self, extracted_text, callback):
        self.root = tk.Tk()
        self.root.title("Markey")
        self.extracted_text = extracted_text
        self.callback = callback
        
        # UI Setup
        self.root.attributes('-topmost', True)
        self.root.geometry("300x250")
        
        # Center Window
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
        self.custom_entry.focus_set()

        # Keyboard shortcuts
        self.root.bind("1", lambda e: self.submit("1"))
        self.root.bind("2", lambda e: self.submit("2"))
        self.root.bind("3", lambda e: self.submit("3"))

    def submit(self, choice):
        topic = self.custom_entry.get()
        self.root.destroy()
        # Send the already-extracted text to the final step
        self.callback(self.extracted_text, choice, topic)

    def show(self):
        self.root.mainloop()