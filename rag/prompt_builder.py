def build_prompt(question, chunks):
    # Build a prompt from retrieved chunks
    context = "\n\n".join(chunk["text"] for chunk in chunks)

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
