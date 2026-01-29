import pdfplumber
import faiss
import numpy as np
import re
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# ================= CONFIG =================
GEMINI_API_KEY = "your_api_key_here"

genai.configure(api_key=GEMINI_API_KEY)

llm = genai.GenerativeModel("gemini-2.5-flash")
embedder = SentenceTransformer("all-MiniLM-L6-v2")
# =========================================


def clean_pdf_text(text):
    text = text.replace("■", "")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\$.*?\$", "", text)
    return text.strip()


def extract_pdf_text(files):
    docs = []

    for file in files:
        with pdfplumber.open(file) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    docs.append({
                        "text": clean_pdf_text(text),
                        "page": i + 1,
                        "source": file.name
                    })

    if not docs:
        raise ValueError("No text extracted from PDFs.")

    return docs


def chunk_text(docs, chunk_size=400, overlap=50):
    chunks = []

    for d in docs:
        words = d["text"].split()
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append({
                "text": chunk,
                "page": d["page"],
                "source": d["source"]
            })

    if not chunks:
        raise ValueError("Chunking failed. No chunks created.")

    return chunks


def build_faiss_index(chunks):
    texts = [c["text"] for c in chunks]

    embeddings = embedder.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    if embeddings.ndim == 1:
        embeddings = embeddings.reshape(1, -1)

    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(embeddings.astype("float32"))

    return index, embeddings, chunks


def search(query, index, chunks, k=4):
    q_emb = embedder.encode([query], convert_to_numpy=True)
    _, indices = index.search(q_emb.astype("float32"), k)
    return [chunks[i] for i in indices[0]]


def generate_llm_answer(question, chunks):
    context = "\n\n".join(
        f"(Page {c['page']}) {c['text']}" for c in chunks
    )

    prompt = f"""
You are an academic assistant.

Answer the question strictly using the provided context.
Do NOT use external knowledge.
If the context is limited, explain clearly what *can* be inferred from it.
The answer MUST be at least 5 complete sentences.
Use simple, clear, educational language.

Context:
{context}

Question:
{question}

Answer:
"""


    response = llm.generate_content(
        prompt,
        generation_config={
            "temperature": 0.2,
            "max_output_tokens": 512
        }
    )

    return response.text.strip()
