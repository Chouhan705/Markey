import asyncio
import io
import os
from PIL import Image, ImageGrab, ImageOps, ImageEnhance
import winrt.windows.media.ocr as ocr
import winrt.windows.graphics.imaging as imaging
import winrt.windows.storage.streams as streams
import winrt.windows.foundation

async def get_text_from_clipboard():
    img_data = ImageGrab.grabclipboard()
    
    if img_data is None:
        return "Error: Clipboard is empty."

    if isinstance(img_data, list):
        img = Image.open(img_data[0])
    else:
        img = img_data
    img = img.convert("L")
    width, height = img.size
    img = img.resize((width * 2, height * 2), Image.Resampling.LANCZOS)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0) 
    img = img.convert("RGB")

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    
    byte_io = io.BytesIO()
    img.save(byte_io, format='PNG')
    image_bytes = byte_io.getvalue()

    stream = streams.InMemoryRandomAccessStream()
    writer = streams.DataWriter(stream.get_output_stream_at(0))
    writer.write_bytes(image_bytes)
    await writer.store_async()
    await writer.flush_async()
    stream.seek(0)

    decoder = await imaging.BitmapDecoder.create_async(stream)
    software_bitmap = await decoder.get_software_bitmap_async()
    engine = ocr.OcrEngine.try_create_from_user_profile_languages()
    
    if not engine:
        return "Error: OCR Engine fail."
        
    result = await engine.recognize_async(software_bitmap)
    return result.text

def run_ocr():
    """Synchronous wrapper to run the async OCR"""
    try:
        return asyncio.run(get_text_from_clipboard())
    except Exception as e:
        return f"Error: {e}"