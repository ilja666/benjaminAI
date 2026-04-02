from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from cacs.environment import SandboxEnvironment
from cacs.memory import EpisodicMemory, SemanticMemory
from cacs.planner import RuleBasedPlanner
from cacs.state import (
    ActionRecord,
    AgentState,
    CognitiveState,
    Episode,
    ObservationRecord,
    ReflectionRecord,
    WorldState,
)


BASE_DIR = Path(__file__).resolve().parents[1]
SCENARIO_PATH = BASE_DIR / "scenarios" / "service_recovery.json"


class TestSandboxEnvironment(unittest.TestCase):
    def test_goal_state_false_when_required_conditions_missing(self) -> None:
        scenario = {
            "goal": {"target_service_state": "running", "required_conditions": {}},
            "world": {
                "objects": {
                    "config": {"type": "file", "state": "valid"},
                    "dependency": {"type": "package", "state": "installed"},
                    "service": {"type": "process", "state": "running"},
                }
            },
            "actions": [],
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "scenario.json"
            path.write_text(json.dumps(scenario), encoding="utf-8")
            env = SandboxEnvironment(path)
            self.assertFalse(env.is_goal_state())

    def test_goal_state_false_when_required_condition_key_unknown(self) -> None:
        scenario = {
            "goal": {
                "target_service_state": "running",
                "required_conditions": {"nonexistent_condition": True},
            },
            "world": {
                "objects": {
                    "config": {"type": "file", "state": "valid"},
                    "dependency": {"type": "package", "state": "installed"},
                    "service": {"type": "process", "state": "running"},
                }
            },
            "actions": [],
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "scenario.json"
            path.write_text(json.dumps(scenario), encoding="utf-8")
            env = SandboxEnvironment(path)
            self.assertFalse(env.is_goal_state())

    def test_start_service_uses_causal_rules_from_scenario(self) -> None:
        env = SandboxEnvironment(SCENARIO_PATH)
        env.execute("fix_config")
        env.execute("install_dependency")
        result = env.execute("start_service")
        self.assertEqual(result["outcome"], "success")
        self.assertEqual(env.world.get_object_state("service"), "running")
        self.assertNotIn("warning", result)


class TestPlannerSemanticMemory(unittest.TestCase):
    def test_planner_uses_remembered_failure_reason(self) -> None:
        world = WorldState(
            objects={
                "config": {"type": "file", "state": "valid"},
                "dependency": {"type": "package", "state": "missing"},
                "service": {"type": "process", "state": "stopped"},
            }
        )
        cognitive_state = CognitiveState(
            world=world,
            agent=AgentState(
                goal={"required_conditions": {}},
                current_strategy="",
                current_hypothesis="",
            ),
        )
        episodic_memory = EpisodicMemory()
        semantic_memory = SemanticMemory()
        episodic_memory.add_episode(
            Episode(
                iteration=1,
                observation=ObservationRecord(summary="obs", details={}),
                action=ActionRecord(name="start_service", action_type="intervene"),
                result={"reason": "missing_dependency", "outcome": "failure"},
                reflection=ReflectionRecord(
                    expectation="Service reaches the running state.",
                    outcome="failure",
                    mismatch=True,
                    explanation="Dependency was missing.",
                ),
            )
        )

        planner = RuleBasedPlanner()
        action = planner.choose_action(cognitive_state, episodic_memory, semantic_memory)

        self.assertEqual(action.name, "install_dependency")
        self.assertEqual(
            cognitive_state.agent.current_strategy,
            "Use remembered mismatch evidence to install the dependency before retrying startup.",
        )
        self.assertEqual(semantic_memory.recall("last_failure_reason"), "missing_dependency")


if __name__ == "__main__":
    unittest.main()
