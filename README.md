# Markey 🚀
**Markey** is a lightweight Windows tool that turns screenshots into LLM-ready Markdown instantly.

## Features
- **OCR Powered:** Uses native Windows OCR (no extra installs).
- **Context Aware:** Choose templates for VS Code errors, GitHub discussions, or custom topics.
- **Background Service:** Sits in the system tray and responds to `Ctrl + Alt + M`.
- **Privacy First:** 100% offline. No data leaves your machine.

## How to Use
1. Run `Markey.exe`.
2. Take a screenshot with `Win + Shift + S`.
3. Press `Ctrl + Alt + M`.
4. Select your format and paste into your favorite LLM.

## Developer Setup Guide
### Follow these steps to configure your local development environment and run Markey from source.

1. Prerequisites
   Ensure you have Python 3.10+ installed on your Windows 10/11 machine.
2. Clone the Repository
   Open your terminal (PowerShell or Command Prompt) and run:
   ```bash
   git clone [https://github.com/yourusername/Markey.git](https://github.com/yourusername/Markey.git)
   cd Markey
3. Install Requirements
   Run:
   ```bash
   pip install winrt-Windows.Media.Ocr winrt-Windows.Graphics.Imaging winrt-Windows.Storage.Streams Pillow keyboard pystray pyperclip
4. Run the Application
   Run:
   ```bash
   python main.py
5. Production Compilation
   To bundle Markey into a portable, zero-dependency single executable file:
   ```bash
   pip install pyinstaller
   pyinstaller --noconsole --onefile --icon=logo.ico --add-data "logo.png;." main.py
