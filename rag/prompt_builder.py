def build_prompt(question, chunks):
    """Build a prompt from the retrieved text chunks."""

    # Combine the retrieved chunks into a single context
    context = "\n\n".join(chunk["text"] for chunk in chunks)

    # Construct the prompt for the language model
    prompt = f"""
You are an expert on Mary Shelly's novel Frankenstein.

Answer the question using ONLY the supplied context.

Rules:
- Do not use outside knowledge.
- If the answer is not contained in the context, reply:
"I don't have enough information."
- Keep your answer cocise (1-5 sentences).

Context:
{context}

Question:
{question}

Answer:
"""

    return prompt
