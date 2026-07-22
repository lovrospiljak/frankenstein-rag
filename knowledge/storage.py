import json
import networkx as nx
import pickle

from knowledge.entities import Entity


def save_json(data, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_entities(
    entities: list[Entity],
    path: str,
) -> None:
    save_json(
        [entity.__dict__ for entity in entities],
        path,
    )


def load_entities(path: str) -> list[Entity]:
    data = load_json(path)
    return [Entity(**entity) for entity in data]


def save_graph(graph, path):
    with open(path, "wb") as f:
        pickle.dump(graph, f)


def load_graph(path):
    with open(path, "rb") as f:
        return pickle.load(f)
