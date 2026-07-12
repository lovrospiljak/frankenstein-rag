CHUNK_SIZE_CHARS = 500
CHUNK_OVERLAP_CHARS = 100


def build_chunks(sections):
    """Split story sections into overlapping text chunks."""

    chunks = []
    chunk_id = 0

    # Calculate the distance between consecutive chunks
    step = CHUNK_SIZE_CHARS - CHUNK_OVERLAP_CHARS

    # Process each story section
    for section in sections:

        text = section["text"]

        # Split the section into overlapping chunks
        for start in range(0, len(text), step):

            chunk_text = text[start : start + CHUNK_SIZE_CHARS].strip()

            # Skip empty chunks
            if not chunk_text:
                continue

            # Store the chunk
            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "section_id": section["section_id"],
                    "text": chunk_text,
                }
            )

            chunk_id += 1

    return chunks
