import textwrap
import re

def normalize_markdown(text: str) -> str:
    # Remove markdown headings
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)

    # Remove bold / italics
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)

    # Convert bullet points
    text = re.sub(r"^\s*[\*\-]\s+", "• ", text, flags=re.MULTILINE)

    # Remove table pipes but keep content
    text = re.sub(r"\|", " ", text)

    # Remove horizontal rules
    text = re.sub(r"^-{3,}$", "", text, flags=re.MULTILINE)

    return text


def wrap_text(text: str, width: int = 90) -> str:
    text = normalize_markdown(text)

    paragraphs = text.split("\n\n")
    wrapped_paragraphs = []

    for para in paragraphs:
        para = para.strip()
        if not para:
            wrapped_paragraphs.append("")
            continue

        wrapped = textwrap.fill(
            para,
            width=width,
            replace_whitespace=False,
            drop_whitespace=False
        )
        wrapped_paragraphs.append(wrapped)

    return "\n\n".join(wrapped_paragraphs)
