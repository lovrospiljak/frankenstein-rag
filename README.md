# Frankenstein-RAG

A Retrieval-Augmented Generation (RAG) system built around **Mary Shelley's _Frankenstein_** to investigate how different retrieval methods affect the consistency of LLM-generated interactive narratives.

> **Research Question:**  
> *Can structured story-world knowledge improve the consistency of LLM-generated interactive narratives compared to a traditional RAG pipeline?*

The ultimate goal of this project is **not only to answer questions about _Frankenstein_, but to generate entirely new interactive narratives that remain faithful to the original story world.**

---

# Project Overview

Large Language Models (LLMs) often generate hallucinations and inconsistencies when answering questions or generating long narratives. Retrieval-Augmented Generation (RAG) addresses this problem by retrieving relevant context before generation.

This project progressively implements and compares three retrieval approaches:

- **Vanilla RAG** – semantic retrieval using vector embeddings and FAISS.
- **GraphRAG** *(planned)* – retrieval enhanced with a knowledge graph.
- **Knowledge-Augmented Generation (KAG)** *(planned)* – combines semantic retrieval with structured story-world knowledge.

All three systems use the **same language model** (**Qwen2.5:3B** running locally with **Ollama**), ensuring that any improvements come from the retrieval strategy rather than the model itself.

The current implementation serves as a **baseline Vanilla RAG system**. While it retrieves relevant passages successfully, the generated answers are not yet consistently grounded in the retrieved context. This baseline will later be compared against GraphRAG and KAG.

---

# Features

## Current

- EPUB parsing
- Story section extraction
- Semantic text chunking
- Embedding generation using **BAAI/bge-base-en-v1.5**
- FAISS vector database
- Semantic similarity retrieval
- Prompt construction
- Local LLM integration using **Ollama**
- Interactive command-line chat application
- Modular project architecture

## Planned

- Knowledge graph construction
- GraphRAG implementation
- Knowledge-Augmented Generation (KAG)
- Interactive narrative generation
- Experimental comparison of Vanilla RAG, GraphRAG and KAG

---

# Project Structure

```text
frankenstein-rag/
│
├── data/
│   ├── processed/
│   │   ├── chunks.json
│   │   ├── embeddings.json
│   │   ├── faiss.index
│   │   └── sections.json
│   │
│   └── raw/
│       └── Frankenstein.epub
│
├── graphrag/                 # Planned
├── kag/                      # Planned
│
├── llm/
│   ├── __init__.py
│   └── local.py
│
├── parser/
│   ├── __init__.py
│   └── epub_parser.py
│
├── rag/
│   ├── __init__.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── prompt_builder.py
│   ├── retriever.py
│   └── vector_store.py
│
├── tests/
│   ├── __init__.py
│   ├── test_local_llm.py
│   ├── test_retrieval.py
│   └── test_rag_pipeline.py
│
├── utils/
│   ├── __init__.py
│   └── storage.py
│
├── .env.example
├── .gitignore
├── build_index.py
├── chat.py
├── config.py
├── LICENSE
├── README.md
└── requirements.txt
```

---

# Technologies

- Python
- Sentence Transformers
- BAAI/bge-base-en-v1.5
- FAISS
- Ollama
- Qwen2.5:3B
- NumPy
- BeautifulSoup4
- EbookLib

---

# Vanilla RAG Pipeline

```text
Frankenstein EPUB
        │
        ▼
 Parse the novel
        │
        ▼
 Split into chunks
        │
        ▼
 Generate embeddings
        │
        ▼
 Store vectors in FAISS
        │
        ▼
 User asks a question
        │
        ▼
 Convert question to embedding
        │
        ▼
 Retrieve relevant chunks
        │
        ▼
 Build prompt
        │
        ▼
 Local LLM (Qwen2.5)
        │
        ▼
 Generated answer
```

---

# Installation

## 1. Clone the repository

```bash
git clone git@github.com:lovrospiljak/frankenstein-rag.git
cd frankenstein-rag
```

## 2. Create a virtual environment

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Install Ollama

Download Ollama from:

https://ollama.com/

Pull the model:

```bash
ollama pull qwen2.5:3b
```

Start the Ollama server:

```bash
ollama serve
```

---

# Usage

## Build the knowledge base

Run once after changing the source novel:

```bash
python build_index.py
```

This script:

- parses the EPUB
- extracts sections
- creates semantic chunks
- generates embeddings
- builds the FAISS vector index

## Start the chat application

```bash
python chat.py
```

Example:

```text
=== Frankenstein RAG ===

> Who created the creature?

Victor Frankenstein created the creature.
```

Type `exit` or `quit` to close the application.

---

# Current Status

The project currently implements a complete **Vanilla RAG pipeline**.

The retrieval stage performs well and successfully finds relevant passages from the novel. However, the generated responses are **not always fully grounded** in the retrieved context. The language model may still rely on its pre-trained knowledge, occasionally producing inconsistent or hallucinated answers.

For example:

```text
> Isn't Frankenstein the monster?

No, Frankenstein is the creator of the monster.

> What is the monster's name?

The monster's name is Frankenstein.
```

This baseline behavior motivates the next stages of the project, where **GraphRAG** and **Knowledge-Augmented Generation (KAG)** will be implemented to improve factual grounding and narrative consistency.

---

# Roadmap

## ✅ Milestone 1 – Data Processing

- EPUB parsing
- Story section extraction

## ✅ Milestone 2 – Vanilla RAG

- Semantic chunking
- Embedding generation
- FAISS vector database
- Semantic retrieval
- Prompt construction
- Local LLM integration
- Interactive chat application

## 🚧 Milestone 3 – GraphRAG

- Knowledge graph construction
- Entity extraction
- Relationship extraction
- Graph-based retrieval

## 📋 Milestone 4 – Knowledge-Augmented Generation (KAG)

- Story-world knowledge representation
- Hybrid retrieval
- Knowledge-guided prompting

## 📋 Milestone 5 – Evaluation

- Compare Vanilla RAG, GraphRAG and KAG
- Measure factual consistency
- Measure narrative consistency
- Analyze hallucination rate

## 📋 Milestone 6 – Interactive Narrative Generation

The final objective is to generate entirely new stories set in the world of **Frankenstein**.

Each retrieval architecture will be extended with a story generation pipeline, allowing direct comparison of the generated narratives.

---

# Research Goal

The project follows a progressive research methodology:

1. Build a **Vanilla RAG** baseline.
2. Extend it into **GraphRAG** using a knowledge graph.
3. Develop a **Knowledge-Augmented Generation (KAG)** system.
4. Compare all three approaches using the **same embedding model** and **same language model**.
5. Evaluate both **question answering** and **interactive narrative generation**.

| System      | Semantic Retrieval | Knowledge Graph | Story-World Knowledge | Status |
|-------------|:------------------:|:---------------:|:---------------------:|:------:|
| Vanilla RAG |         ✅         |        ❌       |          ❌           |   ✅   |
| GraphRAG    |         ✅         |        ✅       |        Partial        |   🚧   |
| KAG         |         ✅         |        ✅       |          ✅           |   🚧   |

---

# License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

See the `LICENSE` file for the complete license text.