# Frankenstein Interactive Narrative with RAG and GraphRAG

## Overview

This project explores Retrieval-Augmented Generation (RAG) techniques for interactive narrative generation using Mary Shelley's *Frankenstein* as the knowledge source.

The system processes the original novel, builds retrieval indexes, and compares two retrieval strategies:

- **Vanilla RAG** using vector similarity search
- **GraphRAG** using a knowledge graph of entities and relationships

Both approaches provide context to a local Large Language Model (LLM), allowing the generation of story continuations while remaining faithful to the source material.

The project serves as the prototype for an AI research internship and will later evolve into a Unity-based interactive narrative game.

---

# Objectives

## Current Objectives

- Parse the Frankenstein EPUB
- Build a retrieval-ready dataset
- Implement Vanilla RAG
- Implement GraphRAG
- Compare retrieval quality
- Generate context-aware story continuations using a local LLM

## Planned Objectives

The project is evolving from a "single continuation generator" into an **interactive narrative engine**.

Instead of producing one long continuation, the system will:

1. Retrieve relevant story context.
2. Generate a short continuation (1–3 sentences).
3. Present exactly three possible actions.
4. Allow the player to choose one.
5. Repeat until the story naturally concludes.

Each complete playthrough should involve approximately **ten player decisions**, enabling a meaningful comparison between Vanilla RAG and GraphRAG over multiple retrieval cycles.

---

# Architecture

```
                    Frankenstein.epub
                            │
                            ▼
                     EPUB Parser
                            │
                            ▼
                      Chunk Builder
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
      Vector Embeddings            Entity Extraction
              │                           │
              ▼                           ▼
         FAISS Index               Knowledge Graph
              │                           │
              └─────────────┬─────────────┘
                            ▼
                    Story Backends
              ┌─────────────┴─────────────┐
              ▼                           ▼
         Vanilla RAG                GraphRAG
              │                           │
              └─────────────┬─────────────┘
                            ▼
                     Story Engine
                            │
                            ▼
                     Local Ollama LLM
```

---

# Current Project Structure

```
frankenstein-rag-v2/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── knowledge/
│
├── rag/
│
├── parser/
│
├── llm/
│
├── scripts/
│
├── story/
│
├── utils/
│
├── config.py
├── main.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

# Current Workflow

1. Parse the EPUB.
2. Split the book into chunks.
3. Generate embeddings.
4. Build a FAISS vector index.
5. Extract named entities.
6. Build a knowledge graph.
7. Choose either:
   - Vanilla RAG
   - GraphRAG
8. Generate a story continuation using the retrieved context.

---

# Planned Gameplay Loop

The next development milestone is to transform the generator into an interactive story.

The intended gameplay loop is:

```
Choose retrieval backend
        │
        ▼
Choose starting scene
        │
        ▼
┌─────────────────────────────┐
│ Retrieve relevant context   │◄──────────────────────────────┐
└─────────────────────────────┘                               │
        │                                                     │
        ▼                                                     │
Generate short story paragraph                               │
        │                                                     │
        ▼                                                     │
Generate three player choices                                │
        │                                                     │
        ▼                                                     │
Player selects one choice                                    │
        │                                                     │
        ▼                                                     │
Update story state                                            │
        │                                                     │
        ▼                                                     │
Story finished? ── No ────────────────────────────────────────┘
        │
       Yes
        │
        ▼
Display ending
```

Unlike the current implementation, the player will **not** enter custom actions. Every turn will consist of selecting one of three AI-generated choices.

---

# Research Goals

The primary research objective is to evaluate whether a knowledge graph improves retrieval quality for interactive storytelling.

The comparison focuses on:

- narrative consistency
- character consistency
- location consistency
- long-term memory
- retrieval relevance
- story coherence across multiple decisions

---

# Technologies

- Python
- Ollama
- Qwen
- FAISS
- NetworkX
- Sentence Transformers
- EPUBLib

---

# Current Status

✅ EPUB parser

✅ Chunk generation

✅ Vector embeddings

✅ FAISS retrieval

✅ Entity extraction

✅ Knowledge graph generation

✅ Vanilla RAG backend

✅ GraphRAG backend

✅ Story generation prototype

---

# Preliminary Results

Initial testing in the terminal has already demonstrated qualitative differences between the two retrieval approaches.

### GraphRAG

During preliminary experiments, GraphRAG consistently generated story continuations that remained faithful to the events of the novel. The generated responses respected the current point in the narrative and maintained consistency with the characters' knowledge and relationships. The generated story continuation was subjectively good and enjoyable to read.

### Vanilla RAG

Vanilla RAG occasionally introduced information from later parts of the novel before those events had occurred. This resulted in temporal inconsistencies and references to future events.

Examples observed during testing include:

> "You have killed my friends, my family!"

At this point in the story, none of these events had yet occurred.

> "... you abandoned me. You left me to suffer, to be hunted, to be despised."

The Creature had only recently been created and had not yet experienced these events.

> "... denied it the love and care it so desperately needed."

Immediately after the Creature's creation, this statement assumes experiences and emotional development that have not yet taken place in the narrative.

These observations suggest that GraphRAG provides stronger narrative consistency than a standard vector-based RAG approach. A systematic evaluation will be performed in future work.

---

# Next Milestones

- Short-form interactive story generation
- AI-generated decision points
- Turn-based gameplay loop
- Story state management across turns
- Automatic story ending after a certain amount of player decisions
- Retrieval quality evaluation