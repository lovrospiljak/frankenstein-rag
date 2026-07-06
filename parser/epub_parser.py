import re

from ebooklib import epub
from ebooklib import ITEM_DOCUMENT
from bs4 import BeautifulSoup

SECTION_PATTERN = re.compile(r"^(Letter|Chapter)\s+(\d+)", re.IGNORECASE)


def extract_section_metadata(text):
    """
    Returns:
        ("letter", 1, "Letter 1")
        ("section", 4, "section 4")
        None
    """

    first_part = text[:300]

    match = SECTION_PATTERN.search(first_part)

    if not match:
        return None

    section_type = match.group(1).lower()
    number = int(match.group(2))
    title = f"{match.group(1).title()} {number}"
    return section_type, number, title


def parse_epub(file_path):
    book = epub.read_epub(file_path)
    sections = []
    section_id = 1

    for item in book.get_items():

        if item.get_type() != ITEM_DOCUMENT:
            continue

        soup = BeautifulSoup(item.get_content(), "html.parser")

        text = soup.get_text(separator=" ", strip=True)

        metadata = extract_section_metadata(text)

        if metadata is None:
            continue

        section_type, number, title = metadata

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
