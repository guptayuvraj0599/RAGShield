from document_processor import load_documents, process_documents
from vector_store import reset_collection, add_documents
from poison_generator import create_poisoned_knowledge_base
from rag_pipeline import answer_query


def build_clean_knowledge_base():
    documents = load_documents()
    processed = process_documents(documents)

    collection = reset_collection("ragshield_clean")
    add_documents(collection, processed)

    print(f"Clean knowledge base created: {len(processed)} chunks")
    return collection


def show_result(title, result):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)
    print("Question:", result["query"])
    print("\nRetrieved evidence:")

    for index, doc in enumerate(result["retrieved_documents"], start=1):
        print(f"\n[{index}] Source: {doc['source']}")
        print("Poisoned:", doc["is_poisoned"])
        print("Text:", doc["text"])
        print("Distance:", doc["distance"])

    print("\nAnswer:")
    print(result["answer"])


def main():
    clean_collection = build_clean_knowledge_base()
    poisoned_collection = create_poisoned_knowledge_base()

    queries = [
        "What time does the university library close?",
        "How many books can a student borrow?",
        "Where should students check examination dates?"
    ]

    for query in queries:
        clean_result = answer_query(
            clean_collection, query, use_llm=True
        )
        poisoned_result = answer_query(
            poisoned_collection, query, use_llm=True
        )

        show_result("CLEAN RAG", clean_result)
        show_result("RAG AFTER POISONING", poisoned_result)


if __name__ == "__main__":
    main()