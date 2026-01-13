from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from datetime import date

def generate_invoice_pdf(data: dict):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y = height - 40

    # ----- HEADER -----
    c.setFont("Helvetica-Bold", 22)
    c.drawString(40, y, "INVOICE")
    y -= 40

    c.setFont("Helvetica", 11)
    c.drawString(40, y, data["seller"])
    y -= 15
    c.drawString(40, y, data["seller_contact"])
    y -= 30

    # ----- CLIENT -----
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Bill To:")
    y -= 15
    c.setFont("Helvetica", 11)
    c.drawString(40, y, data["client"])
    y -= 25

    # ----- INVOICE INFO -----
    c.drawRightString(width - 40, height - 90, f"Invoice #: {data['invoice_no']}")
    c.drawRightString(width - 40, height - 105, f"Date: {data['date']}")

    # ----- TABLE HEADER -----
    y -= 20
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Description")
    c.drawString(300, y, "Qty")
    c.drawString(350, y, "Rate")
    c.drawString(430, y, "Amount")
    y -= 10
    c.line(40, y, width - 40, y)

    # ----- ITEMS -----
    c.setFont("Helvetica", 11)
    y -= 20
    subtotal = 0

    for item in data["items"]:
        amount = item["qty"] * item["rate"]
        subtotal += amount

        c.drawString(40, y, item["desc"])
        c.drawString(300, y, str(item["qty"]))
        c.drawString(350, y, f"{data['currency']} {item['rate']}")
        c.drawString(430, y, f"{data['currency']} {amount}")
        y -= 20

    # ----- TOTALS -----
    y -= 10
    tax = subtotal * data["tax_rate"]
    total = subtotal + tax

    c.line(300, y, width - 40, y)
    y -= 20
    c.drawString(350, y, "Subtotal:")
    c.drawRightString(width - 40, y, f"{data['currency']} {subtotal:.2f}")
    y -= 15
    c.drawString(350, y, "Tax:")
    c.drawRightString(width - 40, y, f"{data['currency']} {tax:.2f}")
    y -= 15
    c.setFont("Helvetica-Bold", 12)
    c.drawString(350, y, "Total:")
    c.drawRightString(width - 40, y, f"{data['currency']} {total:.2f}")

    # ----- FOOTER -----
    y -= 40
    c.setFont("Helvetica", 10)
    c.drawString(40, y, data["notes"])

    c.showPage()
    c.save()

    return buffer.getvalue()
