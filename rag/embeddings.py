# Third-party import
from sentence_transformers import SentenceTransformer

# Load the embedding model
MODEL_NAME = "BAAI/bge-base-en-v1.5"
print(f"Loading embedding model: {MODEL_NAME}")

model = SentenceTransformer(MODEL_NAME)


def embed_text(text):
    """Generate an embedding for a single text."""

    return model.encode(
        text,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )


def embed_chunks(chunks, batch_size=32):
    """Generate embeddings for all text chunks."""

    # Extract the text from each chunk
    texts = [chunk["text"] for chunk in chunks]

    # Generate embeddings in batches
    vectors = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    embeddings = []

    # Combine chunk metadata with the generated embeddings
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
