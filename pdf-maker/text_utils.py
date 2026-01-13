import re

# ---------------- CLEAN RAW TEXT ----------------
def clean_text(text: str) -> str:
    """
    Cleans OCR / clipboard / Gemini text
    """
    if not text:
        return ""

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove weird unicode bullets / boxes
    replacements = {
        "■": "",
        "▪": "",
        "●": "",
        "•": "-",
        "–": "-",
        "—": "-",
        "\u00a0": " ",
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# ---------------- MARKDOWN → TEXT ----------------
def markdown_to_text(text: str) -> str:
    """
    Converts markdown to clean printable text
    """
    if not text:
        return ""

    # Headings
    text = re.sub(r"^#{1,6}\s*(.*)", r"\n\1\n" + "-" * 40, text, flags=re.MULTILINE)

    # Bold / italic
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"_(.*?)_", r"\1", text)

    # Inline code
    text = re.sub(r"`(.*?)`", r"\1", text)

    # Bullet points
    text = re.sub(r"^\s*[-*+]\s+", "- ", text, flags=re.MULTILINE)

    # Numbered lists
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)

    return clean_text(text)
