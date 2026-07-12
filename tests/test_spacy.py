# ----------------------------------------
# Test spaCy Named Entity Recognition.
#
# Run:
# python -m tests.test_spacy
# ----------------------------------------

# Third-party imports
import spacy


def main():
    """Extract named entities from sample text."""

    # Load the English NLP model
    nlp = spacy.load("en_core_web_sm")

    text = """
    Victor Frankenstein created the Creature in Ingolstadt.
    Elizabeth loved Victor.
    Robert Walton sailed to the Arctic.
    """

    # Run Named Entity Recognition
    doc = nlp(text)

    # Display the detected entities
    for ent in doc.ents:
        print(f"{ent.text:<22} {ent.label_}")


if __name__ == "__main__":
    main()
