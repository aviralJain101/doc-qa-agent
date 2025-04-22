# app/ingestion/parsers.py
# Functions to extract raw text from PDF, Markdown, and TXT files

import os
import fitz  # PyMuPDF
import markdown
from bs4 import BeautifulSoup


def parse_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file using PyMuPDF.
    Returns the full concatenated text of all pages.
    """
    text = []
    doc = fitz.open(file_path)
    for page in doc:
        text.append(page.get_text())
    return "\n".join(text)


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
    return soup.get_text(separator="\n")


def parse_txt(file_path: str) -> str:
    """
    Read a plain text file and return its contents.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()



# if __name__ == "__main__":
#     print("PDF:\n", parse_pdf("DocuChat.pdf"))
#     print("MD:\n", parse_md("readme.md"))
#     print("TXT:\n", parse_txt("requirements.txt"))