
from poison_generator import create_poisoned_knowledge_base
from defense_pipeline import defend_query


def main():

    poisoned_collection = create_poisoned_knowledge_base()

    queries = [
        "What time does the university library close?",
        "How many books can a student borrow?",
        "Where should students check examination dates?"
    ]

    print("\n========== RAGSHIELD DEFENSE TEST ==========")

    for query in queries:

        result = defend_query(
            poisoned_collection,
            query,
            use_llm=False
        )

        print("\n----------------------------------------")
        print("FINAL DEFENDED RESPONSE")
        print("----------------------------------------")

        print(result["answer"])

        print("\nSafe documents:",
              len(result["safe_documents"]))

        print("Flagged documents:",
              len(result["flagged_documents"]))


if __name__ == "__main__":
    main()