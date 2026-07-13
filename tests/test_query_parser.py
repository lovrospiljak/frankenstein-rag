# ------------------------------------
# RUN:
# python -m tests.test_query_parser
# ------------------------------------

# Local imports
from knowledge.query_parser import extract_query_terms


def main():
    """Test query term extraction."""

    while True:

        question = input("\nQuestion: ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        terms = extract_query_terms(question)

        print("\nQuery terms:")

        for term in terms:

            print(f"- {term}")


if __name__ == "__main__":
    main()
