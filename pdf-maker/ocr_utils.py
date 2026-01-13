import pytesseract


def extract_text_from_images(images):
    try:
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img) + "\n"
        return text
    except Exception:
        return ""
