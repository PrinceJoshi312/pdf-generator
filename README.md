![License](https://img.shields.io/badge/License-MIT-yellow.svg)


# 📄 PDF Maker Pro

A Streamlit-based web application for generating **professional PDFs** from **text, images, and invoices**, with support for OCR, password protection, watermarks, and cover pages.

---

## ✨ Features

### 📝 Text → PDF

* Convert **plain text or Markdown** into clean PDFs
* Paste text directly (clipboard supported via Ctrl+V)
* Optional **academic formatting**
* Markdown rendering support
* Customizable font size (12–22 pt)
* Optional:

  * Cover page (title, subtitle, footer)
  * Watermark
  * Password protection

---

### 🖼 Image → PDF

* Convert one or more images (PNG, JPG, JPEG) into a single PDF
* Optional **OCR (Optical Character Recognition)**:

  * Extracts text from images
  * Converts extracted text into a text-based PDF
* Supports password-protected image PDFs

---

### 🧾 Invoice → PDF

* Generate professional invoices in PDF format
* Built-in templates:

  * Freelance
  * Company
  * Retail (GST)
  * International
* Features:

  * Itemized billing
  * Automatic totals and tax calculation
  * Currency handling (₹ / USD)
  * Notes section
* Ready-to-send invoice PDFs

---

## 🔐 Security Features

* Password protection for PDFs
* Separate user and owner passwords (where supported)
* Optional permissions:

  * Allow printing
  * Allow copying

---

## 📦 Installation

### Prerequisites

* Python **3.8+**
* pip

### Install Dependencies

```bash
pip install streamlit pillow reportlab PyPDF2 pytesseract
```

> ⚠️ For OCR support, ensure **Tesseract OCR** is installed and available in PATH.

---

## ▶️ Usage

### Run the App

```bash
streamlit run app.py
```

Open in browser:

```
http://localhost:8501
```

---

## 🧭 Application Modes

### Text → PDF

1. Select **Text → PDF**
2. Paste or upload text (`.txt` / `.md`)
3. Choose formatting options
4. Generate and download PDF

---

### Image → PDF

1. Select **Image → PDF**
2. Upload one or more images
3. Optionally enable OCR
4. Generate and download PDF

---

### Invoice → PDF

1. Select **Invoice → PDF**
2. Choose invoice template
3. Enter seller, client, and item details
4. Generate professional invoice PDF

---

## 📁 Project Structure

```
pdf-maker/
├── app.py                 # Main Streamlit application
├── pdf_utils.py           # PDF generation utilities
├── text_utils.py          # Text cleaning & markdown handling
├── invoice_utils.py       # Invoice PDF generation
├── security_utils.py      # PDF password protection
├── ocr_utils.py           # OCR text extraction (optional)
├── requirements.txt       # Dependencies
└── README.md
```

---

## ⚙️ Technical Notes

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![PDF](https://img.shields.io/badge/PDF-Automation-green)

### Text Processing

* Cleans OCR and pasted text automatically
* Markdown is converted to readable PDF-friendly text
* Academic formatting adds section separators

### OCR Behavior

* OCR is optional and auto-disabled if unavailable
* If enabled, images are converted to text PDFs
* If disabled, images are embedded directly

---

## 🧪 Troubleshooting

### OCR Disabled

* Ensure Tesseract OCR is installed
* Restart terminal after installation

### Empty PDF

* Ensure pasted text is not whitespace
* OCR images must contain readable text

### Password Issues

* Passwords are case-sensitive
* No recovery once set

---

## 🚀 Future Improvements (Planned)

* Live PDF preview
* Logo upload for invoices
* Header/footer customization
* Cloud deployment support

---

## 🧠 Built With

* **Streamlit**
* **ReportLab**
* **Pillow**
* **PyPDF2**
* **Tesseract OCR**


## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

**Version:** 1.1.0
**Status:** Stable


