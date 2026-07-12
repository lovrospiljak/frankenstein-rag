# Standard library imports
import json
import re

# Third-party imports
from bs4 import BeautifulSoup
from ebooklib import epub
from ebooklib import ITEM_DOCUMENT

# --------------------------------------------
# Parse an EPUB file into structured sections.
# --------------------------------------------

SECTION_PATTERN = re.compile(r"^(Letter|Chapter)\s+(\d+)", re.IGNORECASE)


def extract_section_metadata(text):
    """
    Returns:
        ("letter", 1, "Letter 1")
        ("section", 4, "section 4")
        None
    """

    # Search only the beginning of the section
    first_part = text[:300]

    match = SECTION_PATTERN.search(first_part)

    if not match:
        return None

    # Extract section information
    section_type = match.group(1).lower()
    number = int(match.group(2))
    title = f"{match.group(1).title()} {number}"

    return section_type, number, title


def parse_epub(file_path):
    """Parse an EPUB file into structured sections."""

    book = epub.read_epub(file_path)

    sections = []
    section_id = 1

    # Process each document in the EPUB
    for item in book.get_items():

        # Skip non-document files
        if item.get_type() != ITEM_DOCUMENT:
            continue

        # Extract plain text from the HTML
        soup = BeautifulSoup(item.get_content(), "html.parser")

        text = soup.get_text(separator=" ", strip=True)

        # Extract section metadata
        metadata = extract_section_metadata(text)

        if metadata is None:
            continue

        section_type, number, title = metadata

        # Store the parsed sections
        sections.append(
            {
                "section_id": section_id,
                "type": section_type,
                "number": number,
                "title": title,
                "source_file": item.get_name(),
                "word_count": len(text.split()),
                "text": text,
            }
        )

        section_id += 1

    return sections


def save_sections(sections, output_path):
    """Save parsed sections to JSON."""

    # Write the JSON file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(sections, f, ensure_ascii=False, indent=4)
