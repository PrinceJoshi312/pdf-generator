from pypdf import PdfReader, PdfWriter
import io

def protect_pdf(
    pdf_bytes: bytes,
    user_password: str,
    owner_password: str | None = None,
    allow_printing: bool = False,
    allow_copying: bool = False,
):
    reader = PdfReader(io.BytesIO(pdf_bytes))
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    permissions = set()
    if allow_printing:
        permissions.add("print")
        
    if allow_copying:
        permissions.add("copy")

    writer.encrypt(
        user_password=user_password,
        owner_password=owner_password or user_password,
        permissions=permissions,
    )

    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()
