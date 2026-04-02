from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .state import Episode


class EpisodicMemory:
    def __init__(self) -> None:
        self._episodes: list[Episode] = []

    def add_episode(self, episode: Episode) -> None:
        self._episodes.append(episode)

    def all_episodes(self) -> list[Episode]:
        return list(self._episodes)

    def latest(self) -> Episode | None:
        if not self._episodes:
            return None
        return self._episodes[-1]

    def recent(self, limit: int = 5) -> list[Episode]:
        return self._episodes[-limit:]

    def find_mismatches(self) -> list[Episode]:
        return [episode for episode in self._episodes if episode.reflection.mismatch]

    def summarize_recent(self, limit: int = 5) -> list[dict[str, Any]]:
        summary: list[dict[str, Any]] = []
        for episode in self.recent(limit):
            summary.append(
                {
                    "iteration": episode.iteration,
                    "action": episode.action.name,
                    "expected": episode.reflection.expectation,
                    "outcome": episode.reflection.outcome,
                    "mismatch": episode.reflection.mismatch,
                }
            )
        return summary

    def to_json(self) -> list[dict[str, Any]]:
        return [asdict(episode) for episode in self._episodes]

    def save(self, path: str | Path) -> None:
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(self.to_json(), indent=2), encoding="utf-8")


class SemanticMemory:
    def __init__(self) -> None:
        self._facts: dict[str, str] = {}

    def remember(self, key: str, value: str) -> None:
        self._facts[key] = value

    def recall(self, key: str) -> str | None:
        return self._facts.get(key)

    def snapshot(self) -> dict[str, str]:
        return dict(self._facts)

    def save(self, path: str | Path) -> None:
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(self.snapshot(), indent=2), encoding="utf-8")
