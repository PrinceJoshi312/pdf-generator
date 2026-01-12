import streamlit as st
from PIL import Image
import pyperclip

from pdf_utils import generate_text_pdf, generate_image_pdf
from text_utils import wrap_text
from security_utils import protect_pdf
from ocr_utils import extract_text_from_images
from ui_components import sidebar, footer

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="PDF Converter Pro",
    page_icon="📄",
    layout="wide"
)

sidebar()

st.markdown("## PDF Converter Pro")
st.caption("Clean, professional PDF generation for text and images")
st.divider()

# ------------------ SESSION STATE INIT ------------------
if "font_size" not in st.session_state:
    st.session_state.font_size = 20
    st.session_state.line_spacing = 26
    st.session_state.margin = 50

# ------------------ TABS ------------------
tab_text, tab_image = st.tabs(["Text → PDF", "Image → PDF"])

# ==================================================
# 📝 TEXT → PDF
# ==================================================
with tab_text:
    left, right = st.columns([1.1, 1.9])

    # ---------- LEFT PANEL ----------
    with left:
        st.markdown("### Document Settings")

        preset = st.radio(
            "Preset",
            ["Custom", "Worksheet", "Answer Key", "Notes"],
            key="preset_radio"
        )

        # Apply presets to session state
        if preset == "Worksheet":
            st.session_state.font_size = 18
            st.session_state.line_spacing = 28
            st.session_state.margin = 60
        elif preset == "Answer Key":
            st.session_state.font_size = 20
            st.session_state.line_spacing = 26
            st.session_state.margin = 50
        elif preset == "Notes":
            st.session_state.font_size = 16
            st.session_state.line_spacing = 24
            st.session_state.margin = 40

        if preset == "Custom":
            st.session_state.font_size = st.slider(
                "Font size", 12, 30, st.session_state.font_size, key="font_slider"
            )
            st.session_state.line_spacing = st.slider(
                "Line spacing", 16, 40, st.session_state.line_spacing, key="line_slider"
            )
            st.session_state.margin = st.slider(
                "Page margin", 30, 80, st.session_state.margin, key="margin_slider"
            )

        st.divider()

        show_footer = st.checkbox("Show page numbers", True, key="footer_text")

        lock_pdf = st.checkbox("Password protect PDF", key="lock_text_pdf")
        password = None
        if lock_pdf:
            password = st.text_input("Password", type="password", key="text_pass")

    # ---------- RIGHT PANEL ----------
    with right:
        st.markdown("### Input")

        uploaded = st.file_uploader("Upload .txt file", type=["txt"])
        use_clipboard = st.checkbox("Use clipboard text", key="clip_text")

        generate_text_btn = st.button(
            "Generate PDF",
            use_container_width=True,
            key="generate_text_pdf"
        )

        if generate_text_btn:
            if use_clipboard:
                raw_text = pyperclip.paste()
                if not raw_text or not raw_text.strip():
                    st.error("Clipboard is empty or contains only whitespace.")
                    st.stop()
            elif uploaded:
                raw_text = uploaded.read().decode("utf-8", errors="ignore")
            else:
                st.warning("Upload a file or enable clipboard text.")
                st.stop()

            wrapped = wrap_text(raw_text)

            with st.spinner("Generating PDF..."):
                pdf = generate_text_pdf(
                    wrapped,
                    st.session_state.font_size,
                    st.session_state.line_spacing,
                    st.session_state.margin,
                    header=None,
                    footer=show_footer
                )

                if lock_pdf and password:
                    pdf = protect_pdf(pdf, password)

            st.success("PDF ready")
            st.download_button(
                "Download PDF",
                pdf,
                "text_output.pdf",
                use_container_width=True
            )

# ==================================================
# 🖼️ IMAGE → PDF
# ==================================================
with tab_image:
    left, right = st.columns([1.1, 1.9])

    with left:
        st.markdown("### Image Options")

        use_ocr = st.checkbox("Extract text using OCR", key="use_ocr")
        lock_pdf_img = st.checkbox("Password protect PDF", key="lock_image_pdf")

        password_img = None
        if lock_pdf_img:
            password_img = st.text_input(
                "Password",
                type="password",
                key="img_pass"
            )

    with right:
        images = st.file_uploader(
            "Upload images",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True
        )

        generate_img_btn = st.button(
            "Generate PDF",
            use_container_width=True,
            key="generate_image_pdf"
        )

        if images and generate_img_btn:
            imgs = [Image.open(i) for i in images]

            with st.spinner("Processing images..."):
                if use_ocr:
                    raw_text = extract_text_from_images(imgs)
                    if not raw_text.strip():
                        st.error("OCR did not detect any text.")
                        st.stop()
                    wrapped = wrap_text(raw_text)
                    pdf = generate_text_pdf(wrapped)
                else:
                    pdf = generate_image_pdf(imgs)

                if lock_pdf_img and password_img:
                    pdf = protect_pdf(pdf, password_img)

            st.success("PDF ready")
            st.download_button(
                "Download PDF",
                pdf,
                "image_output.pdf",
                use_container_width=True
            )

footer()
