import tiktoken

def chunk_text(text: str, max_tokens: int = 300, overlap: int = 100) -> list[str]:
    """
    Split the text into overlapping chunks of ~max_tokens using GPT-3.5 tokenizer.
    """
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)

    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + max_tokens, len(tokens))
        chunk = tokens[start:end]
        chunks.append(encoding.decode(chunk))
        start += max_tokens - overlap

    return chunks

if __name__ == "__main__":
    sample_text = "This is a long piece of text. " * 100
    chunks = chunk_text(sample_text)
    for i, chunk in enumerate(chunks):
        print(f"--- Chunk {i+1} ---\n{chunk}\n")