# ------------------------------------
# Test the local Ollama language model.
#
# Run:
# python -m tests.test_local_llm
# ------------------------------------

# Local imports
from llm.local import generate_answer


def main():
    """Generate a response from the local language model."""

    # Generate a response
    response = generate_answer("Who created the monster?")

    # Display the generated response
    print(response)


if __name__ == "__main__":
    main()
