from PyPDF2 import PdfReader, PdfWriter
import io

def protect_pdf(pdf_bytes, password):
    reader = PdfReader(io.BytesIO(pdf_bytes))
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)

    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()
