from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any



def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ActionRecord:
    name: str
    action_type: str
    expected_outcome: str | None = None
    rationale: str | None = None
    timestamp: str = field(default_factory=utc_now_iso)


@dataclass
class ObservationRecord:
    summary: str
    details: dict[str, Any]
    timestamp: str = field(default_factory=utc_now_iso)


@dataclass
class ReflectionRecord:
    expectation: str
    outcome: str
    mismatch: bool
    explanation: str
    timestamp: str = field(default_factory=utc_now_iso)


@dataclass
class Episode:
    iteration: int
    observation: ObservationRecord
    action: ActionRecord
    result: dict[str, Any]
    reflection: ReflectionRecord
    timestamp: str = field(default_factory=utc_now_iso)


@dataclass
class WorldState:
    objects: dict[str, dict[str, Any]]
    relations: list[dict[str, str]] = field(default_factory=list)

    def get_object_state(self, object_name: str) -> str | None:
        obj = self.objects.get(object_name)
        if obj is None:
            return None
        return obj.get("state")

    def set_object_state(self, object_name: str, new_state: str) -> None:
        if object_name not in self.objects:
            raise KeyError(f"Unknown object: {object_name}")
        self.objects[object_name]["state"] = new_state

    def snapshot(self) -> dict[str, Any]:
        return {
            "objects": {
                name: dict(values)
                for name, values in self.objects.items()
            },
            "relations": [dict(item) for item in self.relations],
        }


@dataclass
class AgentState:
    goal: dict[str, Any]
    current_strategy: str
    current_hypothesis: str
    last_expected_outcome: str | None = None
    last_action: str | None = None
    iteration: int = 0
    status: str = "initialized"

    def advance_iteration(self) -> int:
        self.iteration += 1
        return self.iteration

    def snapshot(self) -> dict[str, Any]:
        return {
            "goal": dict(self.goal),
            "current_strategy": self.current_strategy,
            "current_hypothesis": self.current_hypothesis,
            "last_expected_outcome": self.last_expected_outcome,
            "last_action": self.last_action,
            "iteration": self.iteration,
            "status": self.status,
        }


@dataclass
class CognitiveState:
    world: WorldState
    agent: AgentState

    def snapshot(self) -> dict[str, Any]:
        return {
            "world": self.world.snapshot(),
            "agent": self.agent.snapshot(),
        }
