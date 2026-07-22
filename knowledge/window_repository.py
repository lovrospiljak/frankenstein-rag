"""
Repository for narrative windows.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Window:
    """
    Narrative window.
    """

    window_id: int
    center_chunk_id: int
    chunk_ids: list[int]
    chunk_indices: list[int]
    section_id: int
    text: str
    entities: list[str]


class WindowRepository:
    """
    Repository providing access to narrative windows.
    """

    def __init__(
        self,
        windows_path: str = "data/processed/windows.json",
    ):
        window_file = Path(windows_path)

        if not window_file.exists():
            raise FileNotFoundError(f"Window file not found: {window_file}")

        with open(window_file, encoding="utf-8") as file:
            windows = json.load(file)

        self.lookup = {window["window_id"]: Window(**window) for window in windows}

    def get(
        self,
        window_id: int,
    ) -> Window:

        return self.lookup[window_id]

    def get_many(
        self,
        window_ids: list[int],
    ) -> list[Window]:

        return [self.lookup[window] for window in window_ids if window in self.lookup]

    def get_texts(
        self,
        window_ids: list[int],
    ) -> list[str]:

        return [
            self.lookup[window].text for window in window_ids if window in self.lookup
        ]
