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

## Setup for Developers
1. Clone the repo.
2. Install requirements: `pip install winrt-Windows.Media.Ocr winrt-Windows.Graphics.Imaging winrt-Windows.Storage.Streams Pillow pynput pystray pyperclip`.
3. Run `python main.py`.