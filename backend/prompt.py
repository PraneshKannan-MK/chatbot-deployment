def build_prompt(context_docs, question):
    context = "\n\n".join(
        f"- {doc.page_content}" for doc in context_docs
    )

    return f"""
You are a customer support assistant.
Answer ONLY using the information provided below.
If the answer is not present, say you do not know.

Context:
{context}

Question:
{question}

Answer:
""".strip()