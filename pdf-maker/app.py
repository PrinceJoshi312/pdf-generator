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

from rag_utils import (
    extract_pdf_text,
    chunk_text,
    build_faiss_index,
    search,
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
st.caption("Text • Images • Invoices • Secure • AI PDF Chat")

# ---------- GLOBAL SETTINGS ----------
with st.sidebar:
    st.subheader("⚙ Global Settings")
    font_size = st.slider("Font Size", 12, 22, 12)

# ---------- TABS ----------
tab_text, tab_image, tab_invoice, tab_rag = st.tabs(
    ["📝 Text → PDF", "🖼 Image → PDF", "🧾 Invoice → PDF", "🤖 PDF Chat (RAG)"]
)

# ==================================================
# 📝 TEXT → PDF
# ==================================================
with tab_text:
    uploaded = st.file_uploader("Upload .txt / .md", ["txt", "md"])
    raw_text = uploaded.read().decode("utf-8", errors="ignore") if uploaded else ""

    text = st.text_area("Paste text (Ctrl+V)", raw_text, height=320)

    academic = st.checkbox("🎓 Academic formatting", True)
    markdown = st.checkbox("🧾 Markdown support", True)

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
                    text,
                )

            pdf = generate_text_pdf(text, font_size=font_size)
            st.download_button("⬇ Download PDF", pdf, "text.pdf")

# ==================================================
# 🖼 IMAGE → PDF
# ==================================================
with tab_image:
    images = st.file_uploader(
        "Upload images", ["png", "jpg", "jpeg"], accept_multiple_files=True
    )

    use_ocr = st.checkbox("🧠 Extract text (OCR)", disabled=not OCR_AVAILABLE)

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

            st.download_button("⬇ Download PDF", pdf, "images.pdf")

# ==================================================
# 🧾 INVOICE → PDF
# ==================================================
with tab_invoice:
    seller = st.text_input("Your Name / Company")
    client = st.text_input("Client Name")
    invoice_no = st.text_input(
        "Invoice Number", f"INV-{date.today().strftime('%Y%m%d')}"
    )

    items = []
    for i in range(3):
        desc = st.text_input(f"Item {i+1}")
        qty = st.number_input(f"Qty {i+1}", 0, 100, 1)
        rate = st.number_input(f"Rate {i+1}", 0)
        if desc:
            items.append({"desc": desc, "qty": qty, "rate": rate})

    if st.button("📄 Generate Invoice", use_container_width=True):
        if not seller or not client or not items:
            st.warning("Missing fields")
        else:
            pdf = generate_invoice_pdf({
                "seller": seller,
                "client": client,
                "invoice_no": invoice_no,
                "items": items,
                "date": date.today().strftime("%d %b %Y"),
            })
            st.download_button("⬇ Download Invoice", pdf, "invoice.pdf")

# ==================================================
# 🤖 PDF CHAT (RAG)
# ==================================================
with tab_rag:
    st.subheader("🤖 Chat with your PDFs")
    st.caption("Answers are extracted only from uploaded PDFs")

    if "rag_index" not in st.session_state:
        st.session_state.rag_index = None
        st.session_state.rag_chunks = None

    pdfs = st.file_uploader(
        "Upload PDFs", ["pdf"], accept_multiple_files=True
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📚 Index PDFs", use_container_width=True):
            if not pdfs:
                st.warning("Upload PDFs first")
            else:
                with st.spinner("Indexing..."):
                    docs = extract_pdf_text(pdfs)
                    chunks = chunk_text(docs)
                    index, _, stored = build_faiss_index(chunks)
                    st.session_state.rag_index = index
                    st.session_state.rag_chunks = stored
                st.success("PDFs indexed")

    with col2:
        if st.button("🗑 Clear Index", use_container_width=True):
            st.session_state.rag_index = None
            st.session_state.rag_chunks = None
            st.success("Cleared")

    st.divider()

    if st.session_state.rag_index:
        q = st.text_input("Ask a question from the PDFs")

        if q:
            results = search(
                q,
                st.session_state.rag_index,
                st.session_state.rag_chunks,
                k=5,
            )

            # ---------- FIX 1: Deduplicate ----------
            seen = set()
            unique = []
            for r in results:
                t = r["text"].strip()
                if t and t not in seen:
                    seen.add(t)
                    unique.append(t)

            from rag_utils import generate_llm_answer

            results = search(
                q,
                st.session_state.rag_index,
                st.session_state.rag_chunks,
                k=5
            )

            answer = generate_llm_answer(q, results)

            st.subheader("📘 Answer")
            st.write(answer)

            with st.expander("📎 Sources"):
                for r in results:
                    st.markdown(f"- **{r['source']}** (Page {r['page']})")

# ---------- FOOTER ----------
st.markdown("---")
st.caption("PDF Maker Pro • Text • Images • Invoices • Secure • RAG AI")
