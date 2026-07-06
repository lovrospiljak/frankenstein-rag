from parser.epub_parser import parse_epub
from parser.save_json import save_sections
from rag.chunker import load_sections, build_chunks
from rag.save_chunks import save_chunks
from rag.embeddings import embed_chunks
from rag.save_embeddings import save_embeddings
from rag.vector_store import (
    build_index,
    save_index,
    save_lookup,
)

BOOK_PATH = "data/raw/Frankenstein.epub"

SECTIONS_OUTPUT = "data/processed/sections.json"
CHUNKS_OUTPUT = "data/processed/chunks.json"
EMBEDDINGS_OUTPUT = "data/processed/embeddings.json"


def main():

    # Step 1: Parse the EPUB
    sections = parse_epub(BOOK_PATH)
    print(f"Found {len(sections)} story sections.")

    letters = sum(1 for section in sections if section["type"] == "letter")

    chapters = sum(1 for section in sections if section["type"] == "chapters")

    # Step 2: Save sections
    save_sections(sections, SECTIONS_OUTPUT)
    print(f"Saved story sections to {SECTIONS_OUTPUT}")

    # Step 3: Load sections
    sections = load_sections(SECTIONS_OUTPUT)

    # Step 4: Build chunks
    chunks = build_chunks(sections)

    print(f"Created {len(chunks)} chunks.")

    # Step 5: Save chunks
    save_chunks(chunks, CHUNKS_OUTPUT)
    print(f"Saved chunks to {CHUNKS_OUTPUT}")

    # Step 6: Embeddings
    embeddings = embed_chunks(chunks)
    print(f"Created {len(embeddings)} embeddings.")
    save_embeddings(embeddings, EMBEDDINGS_OUTPUT)

    # Step 7: FAISS vector store
    index = build_index(embeddings)

    save_index(
        index,
        "data/processed/faiss.index",
    )

    save_lookup(
        embeddings,
        "data/processed/chunk_lookup.json",
    )

    print("FAISS index saved.")


if __name__ == "__main__":
    main()
