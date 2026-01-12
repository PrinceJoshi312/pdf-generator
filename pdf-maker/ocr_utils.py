import pytesseract
from PIL import Image

def extract_text_from_images(images):
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img) + "\n"
    return text
