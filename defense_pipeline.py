
from config import TOP_K
from document_processor import load_documents

from rag_pipeline import retrieve_context, build_prompt
from rag_pipeline import generate_with_ollama


from poison_detector import detect_poison


def get_trusted_data():

    clean_documents = load_documents()

    trusted_sources = {
        document.get("source", "unknown")
        for document in clean_documents
    }

    return trusted_sources, clean_documents


def defend_query(collection, query, use_llm=False):

    retrieved_documents = retrieve_context(
        collection,
        query,
        TOP_K
    )

    trusted_sources, trusted_documents = get_trusted_data()

    safe_documents = []
    flagged_documents = []

    print("\n========== RAGSHIELD DEFENSE ENGINE ==========")
    print("\nQuery:", query)

    for document in retrieved_documents:

        detection = detect_poison(
            document,
            trusted_sources,
            trusted_documents
        )

        document["risk_score"] = detection["risk_score"]
        document["risk_level"] = detection["risk_level"]
        document["decision"] = detection["decision"]
        document["reasons"] = detection["reasons"]

        print("\nSource:", document["source"])
        print("Risk Score:", detection["risk_score"])
        print("Risk Level:", detection["risk_level"])
        print("Decision:", detection["decision"])

        if detection["reasons"]:
            for reason in detection["reasons"]:
                print("Reason:", reason)

        if detection["decision"] == "ALLOW":
            safe_documents.append(document)

        else:
            flagged_documents.append(document)

    # Generate answer using only low-risk passages.
    prompt = build_prompt(query, safe_documents)

    if use_llm:
        answer = generate_with_ollama(prompt)
    else:
        answer = (
            "\n".join(
                doc["text"] for doc in safe_documents
            )
            if safe_documents else
            "No sufficiently trusted evidence was available."
        )

    return {
        "query": query,
        "retrieved_documents": retrieved_documents,
        "safe_documents": safe_documents,
        "flagged_documents": flagged_documents,
        "answer": answer
    }