# backend/app/ocr/processor.py

import pytesseract
from PIL import Image
import io
import os

# --- For Windows Users ---
# If you installed Tesseract in a custom location, you might need to specify the path.
# Uncomment the line below and update the path if you get a "tesseract is not installed" error.
# pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_CMD_PATH", r"C:\Program Files\Tesseract-OCR\tesseract.exe")
# -------------------------


def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Uses Tesseract OCR to extract text from an image provided as bytes.
    """
    try:
        # Open the image from the in-memory bytes
        image = Image.open(io.BytesIO(image_bytes))

        # Use pytesseract to extract text
        text = pytesseract.image_to_string(image)

        return text
    except Exception as e:
        print(f"Error during OCR processing: {e}")
        return ""
