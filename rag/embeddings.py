from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-base-en-v1.5"

print(f"Loading embedding model: {MODEL_NAME}")
model = SentenceTransformer(MODEL_NAME)


def embed_chunks(chunks, batch_size=32):
    """
    Generates embeddings for all chunks using batch processing.
    """

    # Extract only the texts
    texts = [chunk["text"] for chunk in chunks]

    # Encode all texts in batches
    vectors = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    embeddings = []

    # Combine metadata with vetors
    for (
        chunk,
        vector,
    ) in zip(chunks, vectors):
        embeddings.append(
            {
                "chunk_id": chunk["chunk_id"],
                "section_id": chunk["section_id"],
                "text": chunk["text"],
                "embedding": vector.tolist(),
            }
        )
    return embeddings
