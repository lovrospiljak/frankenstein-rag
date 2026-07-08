import json


def save_json(data, output_path):

    # Save any Python object as formatted JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4,
        )


def load_json(path):

    # Load JSON from disk
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
