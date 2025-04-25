# app/ingestion/parsers.py
# Functions to extract raw text from PDF, Markdown, and TXT files

import os
import fitz  # PyMuPDF
import markdown
from bs4 import BeautifulSoup
from app.ingestion.normalizer import normalize_text  # Importing normalize_text


def parse_file(file_path: str) -> str:
    """
    Determine file type by extension and route to the appropriate parser.
    Supported formats: .pdf, .md, .txt
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return parse_pdf(file_path)
    elif ext == ".md":
        return parse_md(file_path)
    elif ext == ".txt":
        return parse_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    

def parse_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file using PyMuPDF.
    Returns the full concatenated text of all pages.
    """
    text = []
    doc = fitz.open(file_path)
    for page in doc:
        text.append(page.get_text())
    
    # Normalize the extracted text
    normalized_text = normalize_text("\n".join(text))
    return normalized_text


def parse_md(file_path: str) -> str:
    """
    Read a Markdown file, convert to HTML, then strip HTML tags to get plaintext.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html = markdown.markdown(md_content)
    # Strip HTML tags
    soup = BeautifulSoup(html, "html.parser")
    
    # Normalize the extracted text
    normalized_text = normalize_text(soup.get_text(separator="\n"))
    return normalized_text


def parse_txt(file_path: str) -> str:
    """
    Read a plain text file and return its contents.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    # Normalize the extracted text
    normalized_text = normalize_text(text)
    return normalized_text