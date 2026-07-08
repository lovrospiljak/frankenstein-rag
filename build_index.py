from parser.epub_parser import parse_epub

from rag.chunker import build_chunks
from utils.storage import (
    load_json,
    save_json,
)

from rag.embeddings import embed_chunks

from rag.vector_store import (
    build_index,
    save_index,
)

from utils.storage import save_json

# --------------------------------------------------------
# One-time preprocessing pipeline.
#
# This script:
# 1. Parses the EPUB.
# 2. Splits the novel into chunks.
# 3. Generates embeddings.
# 4. Builds the FAISS vector index.
# --------------------------------------------------------


BOOK_PATH = "data/raw/Frankenstein.epub"

SECTIONS_OUTPUT = "data/processed/sections.json"
CHUNKS_OUTPUT = "data/processed/chunks.json"
EMBEDDINGS_OUTPUT = "data/processed/embeddings.json"
INDEX_OUTPUT = "data/processed/faiss.index"


def main():

    # ----------------------------------------------------
    # Step 1: Parse EPUB
    # ----------------------------------------------------
    sections = parse_epub(BOOK_PATH)

    print(f"Found {len(sections)} story sections.")

    save_json(sections, SECTIONS_OUTPUT)

    print(f"Saved sections to {SECTIONS_OUTPUT}")

    # ----------------------------------------------------
    # Step 2: Load sections and build chunks
    # ----------------------------------------------------
    sections = load_json(SECTIONS_OUTPUT)

    chunks = build_chunks(sections)

    print(f"Created {len(chunks)} chunks.")

    save_json(chunks, CHUNKS_OUTPUT)

    print(f"Saved chunks to {CHUNKS_OUTPUT}")

    # ----------------------------------------------------
    # Step 3: Generate embeddings
    # ----------------------------------------------------
    embeddings = embed_chunks(chunks)

    print(f"Created {len(embeddings)} embeddings.")

    save_json(embeddings, EMBEDDINGS_OUTPUT)

    print(f"Saved embeddings to {EMBEDDINGS_OUTPUT}")

    # ----------------------------------------------------
    # Step 4: Build FAISS index
    # ----------------------------------------------------
    index = build_index(embeddings)

    save_index(
        index,
        INDEX_OUTPUT,
    )

    print(f"Saved FAISS index to {INDEX_OUTPUT}")

    print("\nKnowledge base successfully built.")


if __name__ == "__main__":
    main()
