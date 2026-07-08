from textwrap import wrap

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def build_chunks(sections):
    """
    Split each story section into overlapping chunks.
    """

    chunks = []
    chunk_id = 0

    step = CHUNK_SIZE - CHUNK_OVERLAP

    for section in sections:

        text = section["text"]

        for start in range(0, len(text), step):

            chunk_text = text[start : start + CHUNK_SIZE].strip()

            if not chunk_text:
                continue

            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "section_id": section["section_id"],
                    "text": chunk_text,
                }
            )

            chunk_id += 1

    return chunks
