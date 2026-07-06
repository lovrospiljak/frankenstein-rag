import json


# Only job of this file is to write JSON
def save_sections(sections, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(sections, f, indent=4, ensure_ascii=False)
