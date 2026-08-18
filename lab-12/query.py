"""Lab 12 — Query stage: semantic search + grounded prompt."""
import os
import sys

from ingest import build_collection


def answer_question(question, collection, model, n_results=3):
    # Шаг 1: эмбеддим вопрос той же моделью
    question_embedding = model.encode(question).tolist()

    # Шаг 2: ищем самые похожие чанки
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results,
    )

    retrieved_chunks = results['documents'][0]
    sources = [m['source'] for m in results['metadatas'][0]]

    # Шаг 3: собираем grounded-промпт
    context = "\n\n".join(
        f"[Source: {source}]\n{chunk}"
        for chunk, source in zip(retrieved_chunks, sources)
    )

    prompt = f"""You are a DataShop HR and IT policy assistant.
Answer the question below using ONLY the provided policy excerpts.
If the answer isn't in the excerpts, say "I don't have that information in the provided policies."

Policy Excerpts:
{context}

Question: {question}

Answer:"""

    return prompt, retrieved_chunks, sources


def ask_llm(prompt):
    """Шаг 4: отправляем grounded-промпт в Claude (нужен ANTHROPIC_API_KEY)."""
    import anthropic
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


if __name__ == "__main__":
    model, collection = build_collection()

    questions = sys.argv[1:] or [
        "How many vacation days do I get per year?",
        "What conda environments are approved for data platform work?",
    ]

    use_llm = bool(os.environ.get("ANTHROPIC_API_KEY"))
    if not use_llm:
        print("\n(ANTHROPIC_API_KEY not set — showing retrieved chunks and prompt only)\n")

    for question in questions:
        print("=" * 70)
        print(f"QUESTION: {question}\n")
        prompt, chunks, sources = answer_question(question, collection, model)

        print("RETRIEVED CHUNKS:")
        for source, chunk in zip(sources, chunks):
            print(f"  [{source}] {chunk[:120].strip()!r}...")

        if use_llm:
            print(f"\nANSWER: {ask_llm(prompt)}\n")
        else:
            print(f"\nGROUNDED PROMPT:\n{prompt}\n")
