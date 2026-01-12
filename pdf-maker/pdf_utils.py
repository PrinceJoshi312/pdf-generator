from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
import io

pdfmetrics.registerFont(TTFont("DejaVu", "DejaVuSans.ttf"))



def generate_image_pdf(images, margin=50):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    for img in images:
        img = img.convert("RGB")
        iw, ih = img.size
        scale = min(
            (width - 2 * margin) / iw,
            (height - 2 * margin) / ih
        )
        nw, nh = iw * scale, ih * scale
        x = (width - nw) / 2
        y = (height - nh) / 2

        c.drawInlineImage(img, x, y, nw, nh)
        c.showPage()

    c.save()
    return buffer.getvalue()


def generate_text_pdf(
    text,
    font_size=20,
    line_spacing=26,
    margin=50,
    header=None,
    footer=True
):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    text_obj = c.beginText(margin, height - margin)
    text_obj.setFont("DejaVu", font_size)
    text_obj.setLeading(line_spacing)

    page_number = 1

    for line in text.split("\n"):
        if text_obj.getY() < margin:
            if footer:
                c.drawRightString(
                    width - margin,
                    20,
                    f"Page {page_number}"
                )
            c.showPage()
            page_number += 1
            text_obj = c.beginText(margin, height - margin)
            text_obj.setFont("DejaVu", font_size)
            text_obj.setLeading(line_spacing)

        text_obj.textLine(line)

    c.drawText(text_obj)

    if footer:
        c.drawRightString(width - margin, 20, f"Page {page_number}")

    c.save()
    return buffer.getvalue()
