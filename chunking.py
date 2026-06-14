def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks, preferring breaks at paragraph or sentence boundaries."""
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end == len(text):
            chunks.append(text[start:])
            break
        halfway = start + (end - start) // 2
        cut = end
        for sep in ("\n\n", "\n", ".", "!", "?", " "):
            i = text.rfind(sep, halfway, end)
            if i != -1:
                cut = i + len(sep)
                break
        chunks.append(text[start:cut])
        start = cut - overlap
    return chunks
