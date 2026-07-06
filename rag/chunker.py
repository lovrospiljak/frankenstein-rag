import json


def load_sections(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def chunk_text(text, chunk_size=500, overlap=100):
    """
    Splits text into overlapping word chunks.
    """

    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def build_chunks(sections):
    all_chunks = []
    chunk_id = 1

    for section in sections:
        chunks = chunk_text(section["text"])

        for i, chunk in enumerate(chunks):
            all_chunks.append(
                {
                    "chunk_id": chunk_id,
                    "section_id": section["section_id"],
                    "chunk_index": i,
                    "source_file": section["source_file"],
                    "text": chunk,
                }
            )

            chunk_id += 1

    return all_chunks
