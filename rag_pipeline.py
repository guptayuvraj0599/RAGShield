import json
import urllib.request
import urllib.error

from config import TOP_K
from vector_store import retrieve_documents


def retrieve_context(collection, query, top_k=TOP_K):
    return retrieve_documents(collection, query, top_k)


def build_prompt(query, documents):
    context = "\n\n".join(
        f'Source: {doc["source"]}\n{doc["text"]}'
        for doc in documents
    )

    return f"""
You are a university information assistant.
Answer the question using only the context below.
If the context does not contain the answer, say that you
do not have enough information.

Context:
{context}

Question: {query}

Answer:
"""


def generate_with_ollama(prompt, model="llama3.2:3b"):
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False
    }).encode("utf-8")

    request = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("response", "")
    except (urllib.error.URLError, TimeoutError) as error:
        return (
            "LLM unavailable. Retrieved context is shown below. "
            f"Details: {error}"
        )


def answer_query(collection, query, use_llm=False):
    documents = retrieve_context(collection, query)
    prompt = build_prompt(query, documents)

    if use_llm:
        answer = generate_with_ollama(prompt)
    else:
        answer = (
            "Demo response based on retrieved evidence:\n\n"
            + "\n\n".join(doc["text"] for doc in documents)
            if documents else
            "No relevant documents were retrieved."
        )

    return {
        "query": query,
        "retrieved_documents": documents,
        "prompt": prompt,
        "answer": answer
    }