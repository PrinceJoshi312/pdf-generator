# PDF Converter Pro 📄

A streamlit-based web application for converting text and images into professional, clean PDFs with advanced customization options.

## Features

### Text to PDF Conversion
- Convert plain text files (.txt) to formatted PDFs
- Use clipboard text directly as input
- Multiple preset templates (Worksheet, Answer Key, Notes)
- Full customization control:
  - Font size (12-30pt)
  - Line spacing (16-40pt)
  - Page margins (30-80pt)
- Optional page numbering
- Password protection for sensitive documents

### Image to PDF Conversion
- Convert multiple images (PNG, JPG, JPEG) into a single PDF
- OCR (Optical Character Recognition) support to extract text from images
- Batch processing for multiple images
- Password protection support

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Required Dependencies

```bash
pip install streamlit pillow pyperclip
```

### Additional Dependencies
The application also requires the following custom modules (ensure these are in your project directory):
- `pdf_utils.py` - PDF generation utilities
- `text_utils.py` - Text processing and wrapping
- `security_utils.py` - PDF password protection
- `ocr_utils.py` - OCR text extraction
- `ui_components.py` - Sidebar and footer components

## Usage

### Starting the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Text to PDF Workflow

1. Navigate to the **Text → PDF** tab
2. Configure document settings:
   - Select a preset (Worksheet, Answer Key, Notes) or use Custom settings
   - Adjust font size, line spacing, and margins as needed
   - Toggle page numbers on/off
   - Optionally enable password protection
3. Provide input text:
   - Upload a .txt file, OR
   - Enable "Use clipboard text" to paste from clipboard
4. Click **Generate PDF**
5. Download your formatted PDF

### Image to PDF Workflow

1. Navigate to the **Image → PDF** tab
2. Configure options:
   - Enable "Extract text using OCR" to convert image text to formatted PDF
   - Optionally enable password protection
3. Upload one or more image files (PNG, JPG, JPEG)
4. Click **Generate PDF**
5. Download your PDF

## Preset Templates

### Worksheet
- Font size: 18pt
- Line spacing: 28pt
- Margin: 60pt
- Ideal for: Student worksheets, practice exercises

### Answer Key
- Font size: 20pt
- Line spacing: 26pt
- Margin: 50pt
- Ideal for: Answer sheets, reference documents

### Notes
- Font size: 16pt
- Line spacing: 24pt
- Margin: 40pt
- Ideal for: Study notes, compact documents

## Security Features

The application supports password-protecting generated PDFs. When enabled:
- The PDF will require a password to open
- Useful for sensitive documents or answer keys
- Separate password options for text and image PDFs

## Project Structure

```
pdf-converter-pro/
├── app.py                 # Main application file
├── pdf_utils.py          # PDF generation functions
├── text_utils.py         # Text processing utilities
├── security_utils.py     # PDF encryption/protection
├── ocr_utils.py          # OCR text extraction
├── ui_components.py      # UI helper components
└── requirements.txt      # Python dependencies
```

## Technical Details

### Session State Management
The application uses Streamlit's session state to maintain settings across interactions:
- `font_size`: Current font size setting
- `line_spacing`: Current line spacing setting
- `margin`: Current page margin setting

### Text Processing
Text input is automatically wrapped to fit page dimensions based on the configured settings, ensuring proper formatting across all pages.

### OCR Processing
When OCR is enabled for images, the application extracts text from uploaded images and converts it to a formatted text PDF rather than embedding the images directly.

## Troubleshooting

### Empty Clipboard Error
If you see "Clipboard is empty or contains only whitespace":
- Ensure you've copied text to your clipboard before enabling the clipboard option
- Try copying the text again

### OCR No Text Detected
If OCR doesn't detect text:
- Verify the image contains readable text
- Ensure the image quality is sufficient
- Try adjusting image contrast or resolution

### Password Protection Issues
- Passwords are case-sensitive
- Ensure you remember the password - there's no recovery option
- Test the password immediately after generation

## Contributing

To extend or modify the application:
1. Fork the repository
2. Create a feature branch
3. Implement changes in the appropriate utility module
4. Test thoroughly with various input types
5. Submit a pull request

## License

This project is provided as-is for educational and professional use.

## Support

For issues, questions, or feature requests, please open an issue in the project repository.

---

**Version:** 1.0.0  
**Built with:** Streamlit, Pillow, PyPDF2/ReportLab
