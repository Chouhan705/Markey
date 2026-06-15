import asyncio
import io
import sys
from PIL import Image, ImageGrab, ImageOps

# Centralized framework imports 
import winrt.windows.media.ocr as ocr
import winrt.windows.graphics.imaging as imaging
import winrt.windows.storage.streams as streams

async def get_text_from_clipboard():
    # 1. Capture Raw Clipboard Asset
    img_data = ImageGrab.grabclipboard()
    if img_data is None:
        return "Error: Clipboard is empty. Snip something first!"

    img = img_data if not isinstance(img_data, list) else Image.open(img_data[0])

    # === SAFE RGBA FLATTENING LOGIC STACK ===
    # Check if image has an alpha/transparency channel and flatten it 
    # to prevent Pillow's ImageOps from crashing on certain screenshots.
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        # Create a solid black background
        bg = Image.new("RGB", img.size, (0, 0, 0))
        # Separate the alpha channel to use as a blend mask
        mask = img.convert("RGBA").split()[3]
        bg.paste(img, mask=mask)
        img = bg
    else:
        # Guarantee standard 24-bit RGB pixel structure
        img = img.convert("RGB")
    # ========================================

    # Clean multi-monitor upscaling pipeline
    if img.width < 1000:
        img = img.resize((img.width * 2, img.height * 2), Image.Resampling.BICUBIC)
    
    # Safe to call now without throwing exceptions
    img = ImageOps.autocontrast(img, cutoff=1)

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
        return "Error: OCR Engine failing initialization context."
    
    result = await engine.recognize_async(software_bitmap)

    lines_raw = []
    for line in result.lines:
        if not line.words:
            continue
        line_text = " ".join([w.text for w in line.words])
        avg_h = sum([w.bounding_rect.height for w in line.words]) / len(line.words)
        lines_raw.append({"text": line_text, "height": avg_h})

    if not lines_raw:
        return ""

    heights = [l["height"] for l in lines_raw]
    avg_base_height = sum(heights) / len(heights)

    formatted_md = []
    for line in lines_raw:
        if line["height"] > avg_base_height * 1.35:
            prefix = "### "
        elif line["height"] > avg_base_height * 1.15:
            prefix = "#### "
        else:
            prefix = ""
            
        formatted_md.append(f"{prefix}{line['text']}".strip())

    return "\n".join(formatted_md)

def run_ocr():
    try:
        return asyncio.run(get_text_from_clipboard())
    except Exception as e:
        return f"Error: {e}"