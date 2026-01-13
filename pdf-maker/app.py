import streamlit as st
from PIL import Image
import re
from datetime import date

# ---------- INTERNAL IMPORTS ----------
from pdf_utils import (
    generate_text_pdf,
    generate_image_pdf,
    generate_cover_page,
    apply_watermark,
)
from text_utils import clean_text, markdown_to_text
from security_utils import protect_pdf
from invoice_utils import generate_invoice_pdf

# OCR (optional)
try:
    from ocr_utils import extract_text_from_images
    OCR_AVAILABLE = True
except Exception:
    OCR_AVAILABLE = False

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="PDF Maker Pro",
    page_icon="📄",
    layout="wide"
)

st.title("📄 PDF Maker Pro")
st.caption("Text • Images • Invoices • Secure PDFs")

# ---------- SIDEBAR ----------
mode = st.sidebar.radio(
    "Choose Mode",
    ["Text → PDF", "Image → PDF", "Invoice → PDF"]
)

font_size = st.sidebar.slider(
    "Font Size",
    min_value=12,
    max_value=22,
    value=12
)

# ==================================================
# 📝 TEXT → PDF
# ==================================================
if mode == "Text → PDF":
    st.subheader("📝 Text / Markdown to PDF")

    uploaded = st.file_uploader(
        "Upload .txt / .md file",
        type=["txt", "md"]
    )

    raw_text = uploaded.read().decode("utf-8", errors="ignore") if uploaded else ""

    text = st.text_area(
        "Paste text here (Ctrl+V supported)",
        value=raw_text,
        height=320
    )

    academic = st.checkbox("🎓 Academic formatting", True)
    markdown = st.checkbox("🧾 Markdown support", True)

    st.divider()
    st.subheader("🔐 Security & Layout")

    use_cover = st.checkbox("📘 Add cover page")
    cover_title = cover_sub = cover_footer = ""
    if use_cover:
        cover_title = st.text_input("Cover title")
        cover_sub = st.text_input("Subtitle")
        cover_footer = st.text_input("Footer")

    watermark = st.checkbox("💧 Watermark")
    watermark_text = st.text_input("Watermark text") if watermark else ""

    lock_pdf = st.checkbox("🔐 Password protect PDF")
    user_pw = owner_pw = None
    allow_print = allow_copy = False

    if lock_pdf:
        user_pw = st.text_input("User password", type="password")
        owner_pw = st.text_input("Owner password (optional)", type="password")
        allow_print = st.checkbox("Allow printing")
        allow_copy = st.checkbox("Allow copying")

    if st.button("📄 Generate PDF", use_container_width=True):
        if not text.strip():
            st.warning("No text provided.")
        else:
            text = clean_text(text)
            if markdown:
                text = markdown_to_text(text)

            if academic:
                text = re.sub(
                    r"(UNIT\s+[IVX]+|Section\s+[A-Z])",
                    r"\n\n\1\n" + "-" * 40,
                    text
                )

            pdf = generate_text_pdf(text, font_size=font_size)

            if use_cover:
                pdf = generate_cover_page(
                    cover_title, cover_sub, cover_footer
                ) + pdf

            if watermark and watermark_text:
                pdf = apply_watermark(pdf, watermark_text)

            if lock_pdf and user_pw:
                pdf = protect_pdf(
                    pdf, user_pw, owner_pw, allow_print, allow_copy
                )

            st.success("PDF generated")
            st.download_button("⬇ Download PDF", pdf, "text.pdf")

# ==================================================
# 🖼 IMAGE → PDF
# ==================================================
elif mode == "Image → PDF":
    st.subheader("🖼 Image to PDF")
    st.info("Paste images using Ctrl+V or upload files")

    images = st.file_uploader(
        "Upload images",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    use_ocr = st.checkbox(
        "🧠 Extract text (OCR)",
        disabled=not OCR_AVAILABLE
    )

    lock_img = st.checkbox("🔐 Password protect PDF")
    img_pw = st.text_input("Password", type="password") if lock_img else None

    if images:
        pil_images = [Image.open(i).convert("RGB") for i in images]
        st.image(pil_images, width=150)

        if st.button("📄 Generate Image PDF", use_container_width=True):
            if use_ocr and OCR_AVAILABLE:
                text = extract_text_from_images(pil_images)
                text = clean_text(text)
                pdf = generate_text_pdf(text, font_size=font_size)
            else:
                pdf = generate_image_pdf(pil_images)

            if lock_img and img_pw:
                pdf = protect_pdf(pdf, img_pw)

            st.success("PDF generated")
            st.download_button("⬇ Download PDF", pdf, "images.pdf")

# ==================================================
# 🧾 INVOICE → PDF
# ==================================================
elif mode == "Invoice → PDF":
    st.subheader("🧾 Invoice Generator")

    template = st.selectbox(
        "Invoice Template",
        ["Freelance", "Company", "Retail (GST)", "International"]
    )

    col1, col2 = st.columns(2)
    with col1:
        seller = st.text_input("Your Name / Company")
        contact = st.text_input("Contact Details")
    with col2:
        client = st.text_input("Client Name")
        invoice_no = st.text_input(
            "Invoice Number",
            f"INV-{date.today().strftime('%Y%m%d')}"
        )

    currency = "₹"
    tax_rate = 0.0
    if template == "Retail (GST)":
        tax_rate = st.slider("GST %", 0, 28, 18) / 100
    elif template == "International":
        currency = "USD"
        tax_rate = st.slider("Tax %", 0, 30, 0) / 100

    st.subheader("Items")
    items = []
    for i in range(3):
        c1, c2, c3 = st.columns(3)
        desc = c1.text_input(f"Description {i+1}")
        qty = c2.number_input(f"Qty {i+1}", min_value=0, step=1)
        rate = c3.number_input(f"Rate {i+1}", min_value=0)

        if desc:
            items.append({"desc": desc, "qty": qty, "rate": rate})

    notes = st.text_area("Notes", "Thank you for your business!")

    if st.button("📄 Generate Invoice PDF", use_container_width=True):
        if not seller or not client or not items:
            st.warning("Fill all required fields.")
        else:
            data = {
                "seller": seller,
                "seller_contact": contact,
                "client": client,
                "invoice_no": invoice_no,
                "date": date.today().strftime("%d %b %Y"),
                "items": items,
                "tax_rate": tax_rate,
                "currency": currency,
                "notes": notes,
            }

            pdf = generate_invoice_pdf(data)

            st.success("Invoice generated")
            st.download_button(
                "⬇ Download Invoice",
                pdf,
                "invoice.pdf"
            )


# ---------- FOOTER ----------
st.markdown("---")
st.caption("PDF Maker Pro • Text • Images • Invoices • Secure")
