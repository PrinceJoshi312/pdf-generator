# pdf_utils.py
from io import BytesIO
import os

from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

# ---------------- FONT REGISTRATION ----------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(BASE_DIR, "fonts")

REGULAR_FONT = os.path.join(FONT_DIR, "DejaVuSans.ttf")
BOLD_FONT = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

pdfmetrics.registerFont(TTFont("DejaVu", REGULAR_FONT))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", BOLD_FONT))

# ---------------- STYLES ----------------

styles = getSampleStyleSheet()

BODY_STYLE = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontName="DejaVu",
    fontSize=12,
    leading=12,
    spaceBefore=0,
    spaceAfter=0
)

HEADING_STYLE = ParagraphStyle(
    "Heading",
    parent=styles["Normal"],
    fontName="DejaVu-Bold",
    fontSize=18,
    leading=18,
    spaceBefore=6,
    spaceAfter=6
)

# ---------------- TEXT → PDF ----------------

def generate_text_pdf(
    text,
    font_size=12,
    line_spacing=None,
    margin=0
):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    import io

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    x = margin
    y = height - margin

    if line_spacing is None:
        line_spacing = font_size + 2

    c.setFont("Helvetica", font_size)

    for line in text.split("\n"):
        if y <= margin:
            c.showPage()
            c.setFont("Helvetica", font_size)
            y = height - margin
        c.drawString(x, y, line)
        y -= line_spacing

    c.save()
    buffer.seek(0)
    return buffer.getvalue()


# ---------------- IMAGE → PDF ----------------

def generate_image_pdf(images) -> bytes:
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0,
        leftMargin=0,
        topMargin=0,
        bottomMargin=0
    )

    story = []

    for img in images:
        img_io = BytesIO()
        img.save(img_io, format="PNG")
        img_io.seek(0)

        image = Image(img_io)
        image._restrictSize(A4[0], A4[1])
        story.append(image)

    doc.build(story)
    return buffer.getvalue()


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

def apply_watermark(pdf_bytes: bytes, watermark_text: str):
    from pypdf import PdfReader, PdfWriter

    reader = PdfReader(io.BytesIO(pdf_bytes))
    writer = PdfWriter()

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica-Bold", 40)
    can.setFillGray(0.85)
    can.saveState()
    can.translate(300, 400)
    can.rotate(45)
    can.drawCentredString(0, 0, watermark_text)
    can.restoreState()
    can.save()

    packet.seek(0)
    watermark = PdfReader(packet).pages[0]

    for page in reader.pages:
        page.merge_page(watermark)
        writer.add_page(page)

    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()


def generate_cover_page(title, subtitle="", footer=""):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter


    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width / 2, height - 200, title)

    if subtitle:
        c.setFont("Helvetica", 16)
        c.drawCentredString(width / 2, height - 260, subtitle)

    if footer:
        c.setFont("Helvetica", 12)
        c.drawCentredString(width / 2, 100, footer)

    c.showPage()
    c.save()

    return buffer.getvalue()
