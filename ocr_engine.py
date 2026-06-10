import asyncio
import io
from PIL import Image, ImageGrab, ImageEnhance
import winrt.windows.media.ocr as ocr
import winrt.windows.graphics.imaging as imaging
import winrt.windows.storage.streams as streams

async def get_text_from_clipboard():
    # 1. Capture Image
    img_data = ImageGrab.grabclipboard()
    if img_data is None:
        return "Error: Clipboard is empty. Snip something first!"

    img = img_data if not isinstance(img_data, list) else Image.open(img_data[0])

    # 2. Preprocessing Pipeline for Ultra-Sharp OCR Accuracy
    img = img.convert("L")  # Convert to Grayscale
    width, height = img.size
    img = img.resize((width * 2, height * 2), Image.Resampling.LANCZOS) # High fidelity Upscale
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0).convert("RGB") # Extreme Contrast Separation

    # 3. Memory Stream to WinRT
    byte_io = io.BytesIO()
    img.save(byte_io, format='PNG')
    image_bytes = byte_io.getvalue()

    stream = streams.InMemoryRandomAccessStream()
    writer = streams.DataWriter(stream.get_output_stream_at(0))
    writer.write_bytes(image_bytes)
    await writer.store_async()
    await writer.flush_async()
    stream.seek(0)

    # 4. Initialize Core Engine
    decoder = await imaging.BitmapDecoder.create_async(stream)
    software_bitmap = await decoder.get_software_bitmap_async()
    engine = ocr.OcrEngine.try_create_from_user_profile_languages()
    if not engine:
        return "Error: OCR Engine failing initialization context."
    
    result = await engine.recognize_async(software_bitmap)

    # 5. Semantic Extractor / Dynamic Bucket Sorting
    lines_raw = []
    for line in result.lines:
        if not line.words:
            continue
        line_text = " ".join([w.text for w in line.words])
        avg_h = sum([w.bounding_rect.height for w in line.words]) / len(line.words)
        lines_raw.append({"text": line_text, "height": avg_h})

    if not lines_raw:
        return ""

    # Group baseline deviations to the nearest factor of 10 to clear noise
    unique_heights = sorted(list(set([round(l["height"], -1) for l in lines_raw])), reverse=True)
    
    height_to_header = {}
    for i, h in enumerate(unique_heights):
        if i < 6 and len(unique_heights) > 1:
            height_to_header[h] = "#" * (i + 1)
        else:
            height_to_header[h] = ""

    formatted_md = []
    for line in lines_raw:
        h_bucket = round(line["height"], -1)
        prefix = height_to_header.get(h_bucket, "")
        formatted_md.append(f"{prefix} {line['text']}".strip())

    return "\n".join(formatted_md)

def run_ocr():
    try:
        return asyncio.run(get_text_from_clipboard())
    except Exception as e:
        return f"Error: {e}"