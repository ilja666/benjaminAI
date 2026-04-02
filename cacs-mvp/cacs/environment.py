from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .state import WorldState


class SandboxEnvironment:
    def __init__(self, scenario_path: str | Path) -> None:
        self.scenario_path = Path(scenario_path)
        self.scenario = self._load_scenario(self.scenario_path)
        self.goal = self.scenario["goal"]
        self.available_actions = {action["name"]: action for action in self.scenario["actions"]}
        self.causal_rules = self.scenario.get("causal_rules", [])
        self.world = WorldState(
            objects=self.scenario["world"]["objects"],
            relations=self.scenario["world"].get("relations", []),
        )

    def _current_conditions(self) -> dict[str, Any]:
        return {
            "config_valid": self.world.get_object_state("config") == "valid",
            "dependency_installed": self.world.get_object_state("dependency") == "installed",
            "service_running": self.world.get_object_state("service") == "running",
            "config": self.world.get_object_state("config"),
            "dependency": self.world.get_object_state("dependency"),
            "service": self.world.get_object_state("service"),
        }

    def _apply_effects(self, effects: list[dict[str, Any]]) -> None:
        for effect in effects:
            self.world.set_object_state(effect["object"], effect["new_state"])

    def _matches_rule(self, action_name: str, rule: dict[str, Any]) -> bool:
        conditions = dict(rule.get("if", {}))
        if conditions.get("action") != action_name:
            return False

        current = self._current_conditions()
        for key, expected in conditions.items():
            if key == "action":
                continue
            if current.get(key) != expected:
                return False
        return True

    def _apply_causal_rule(self, action_name: str) -> dict[str, Any] | None:
        for rule in self.causal_rules:
            if not self._matches_rule(action_name, rule):
                continue

            consequence = dict(rule.get("then", {}))
            state_updates = []
            for object_name, new_state in consequence.items():
                if object_name in self.world.objects:
                    state_updates.append({"object": object_name, "new_state": new_state})

            if state_updates:
                self._apply_effects(state_updates)

            outcome = consequence.get("outcome", "success")
            result: dict[str, Any] = {
                "action": action_name,
                "type": self.available_actions[action_name]["type"],
                "outcome": outcome,
                "world": self.world.snapshot(),
                "goal_reached": self.is_goal_state(),
            }
            if "reason" in consequence:
                result["reason"] = consequence["reason"]
            return result
        return None

    def _goal_evaluation(self) -> tuple[bool, str | None]:
        required_conditions = self.goal.get("required_conditions", {})
        if not required_conditions:
            return False, "Goal is missing required_conditions or defines none."

        current = self._current_conditions()
        unknown_keys = [key for key in required_conditions if key not in current]
        if unknown_keys:
            return False, f"Unknown goal condition keys: {', '.join(unknown_keys)}"

        return (
            all(current[key] == value for key, value in required_conditions.items()),
            None,
        )

    def _load_scenario(self, path: Path) -> dict[str, Any]:
        return json.loads(path.read_text(encoding="utf-8"))

    def observe(self) -> dict[str, Any]:
        return {
            "world": self.world.snapshot(),
            "goal": self.goal,
            "available_actions": list(self.available_actions.keys()),
        }

    def is_goal_state(self) -> bool:
        goal_reached, _ = self._goal_evaluation()
        return goal_reached

    def execute(self, action_name: str) -> dict[str, Any]:
        if action_name not in self.available_actions:
            raise ValueError(f"Unknown action: {action_name}")

        action = self.available_actions[action_name]
        if action["type"] == "observe":
            return {
                "action": action_name,
                "type": "observe",
                "outcome": "observed",
                "world": self.world.snapshot(),
                "goal_reached": self.is_goal_state(),
            }

        if action_name == "start_service":
            causal_result = self._apply_causal_rule(action_name)
            if causal_result is not None:
                return causal_result
            return self._attempt_start_service(action_name)

        self._apply_effects(action.get("effects", []))

        return {
            "action": action_name,
            "type": action["type"],
            "outcome": "success",
            "world": self.world.snapshot(),
            "goal_reached": self.is_goal_state(),
        }

    def _attempt_start_service(self, action_name: str) -> dict[str, Any]:
        config_state = self.world.get_object_state("config")
        dependency_state = self.world.get_object_state("dependency")

        if config_state != "valid":
            self.world.set_object_state("service", "stopped")
            return {
                "action": action_name,
                "type": "intervene",
                "outcome": "failure",
                "reason": "invalid_config",
                "world": self.world.snapshot(),
                "goal_reached": False,
                "warning": "Fallback engine path used because no matching causal rule was found.",
            }

        if dependency_state != "installed":
            self.world.set_object_state("service", "stopped")
            return {
                "action": action_name,
                "type": "intervene",
                "outcome": "failure",
                "reason": "missing_dependency",
                "world": self.world.snapshot(),
                "goal_reached": False,
                "warning": "Fallback engine path used because no matching causal rule was found.",
            }

        self.world.set_object_state("service", "running")
        return {
            "action": action_name,
            "type": "intervene",
            "outcome": "success",
            "world": self.world.snapshot(),
            "goal_reached": self.is_goal_state(),
            "warning": "Fallback engine path used because no matching causal rule was found.",
        }

    def allowed_actions(self) -> list[str]:
        return list(self.available_actions.keys())
