# Standard library import
import json


def save_json(data, output_path):
    """Save data to a JSON file."""

    # Write the JSON file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4,
        )


def load_json(path):
    """Load data from a JSON file."""

    # Read the JSON file
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
