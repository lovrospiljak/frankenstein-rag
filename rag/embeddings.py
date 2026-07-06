from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-base-en-v1.5"

print(f"Loading embedding model: {MODEL_NAME}")
model = SentenceTransformer(MODEL_NAME)


import time


def embed_chunks(chunks, batch_size=32):
    texts = [chunk["text"] for chunk in chunks]

    start = time.time()

    vectors = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    print(f"\nEmbedding model took {time.time() - start:.2f} seconds")

    embeddings = []

    for chunk, vector in zip(chunks, vectors):
        embeddings.append(
            {
                "chunk_id": chunk["chunk_id"],
                "section_id": chunk["section_id"],
                "text": chunk["text"],
                "embedding": vector.tolist(),
            }
        )

    return embeddings
