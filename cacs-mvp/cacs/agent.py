from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from .environment import SandboxEnvironment
from .memory import EpisodicMemory, SemanticMemory
from .planner import RuleBasedPlanner
from .reflection import ReflectionEngine
from .state import AgentState, CognitiveState, Episode, ObservationRecord


class CACSAgent:
    def __init__(self, environment: SandboxEnvironment) -> None:
        self.environment = environment
        self.episodic_memory = EpisodicMemory()
        self.semantic_memory = SemanticMemory()
        self.planner = RuleBasedPlanner()
        self.reflection_engine = ReflectionEngine()
        self.cognitive_state = CognitiveState(
            world=environment.world,
            agent=AgentState(
                goal=environment.goal,
                current_strategy="Establish the initial state of the sandbox.",
                current_hypothesis="The service is blocked by one or more unmet prerequisites.",
                status="ready",
            ),
        )

    def sense(self) -> ObservationRecord:
        observation = self.environment.observe()
        summary = (
            f"Observed config={self.cognitive_state.world.get_object_state('config')}, "
            f"dependency={self.cognitive_state.world.get_object_state('dependency')}, "
            f"service={self.cognitive_state.world.get_object_state('service')}"
        )
        return ObservationRecord(summary=summary, details=observation)

    def run_iteration(self) -> Episode:
        iteration = self.cognitive_state.agent.advance_iteration()
        observation = self.sense()
        action = self.planner.choose_action(
            self.cognitive_state,
            self.episodic_memory,
            self.semantic_memory,
        )
        self.cognitive_state.agent.last_action = action.name
        result = self.environment.execute(action.name)
        reflection = self.reflection_engine.reflect(action.expected_outcome, result)

        episode = Episode(
            iteration=iteration,
            observation=observation,
            action=action,
            result=result,
            reflection=reflection,
        )
        self.episodic_memory.add_episode(episode)

        if reflection.mismatch and result.get("reason"):
            self.semantic_memory.remember(
                f"iteration_{iteration}_failure_reason",
                str(result.get("reason")),
            )

        if result.get("goal_reached"):
            self.cognitive_state.agent.status = "goal_reached"
        else:
            self.cognitive_state.agent.status = "running"

        return episode

    def run(self, max_iterations: int = 10) -> dict[str, Any]:
        episodes: list[dict[str, Any]] = []
        for _ in range(max_iterations):
            episode = self.run_iteration()
            episodes.append(asdict(episode))
            if self.environment.is_goal_state():
                break

        return {
            "goal_reached": self.environment.is_goal_state(),
            "iterations": self.cognitive_state.agent.iteration,
            "agent_state": self.cognitive_state.agent.snapshot(),
            "world_state": self.cognitive_state.world.snapshot(),
            "episodes": episodes,
            "semantic_memory": self.semantic_memory.snapshot(),
        }

    def save_artifacts(self, output_dir: str | Path) -> None:
        destination = Path(output_dir)
        destination.mkdir(parents=True, exist_ok=True)
        self.episodic_memory.save(destination / "episodic_memory.json")
        self.semantic_memory.save(destination / "semantic_memory.json")
