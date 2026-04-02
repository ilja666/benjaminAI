from __future__ import annotations

from .memory import EpisodicMemory, SemanticMemory
from .state import ActionRecord, CognitiveState


class RuleBasedPlanner:
    def choose_action(
        self,
        cognitive_state: CognitiveState,
        episodic_memory: EpisodicMemory,
        semantic_memory: SemanticMemory,
    ) -> ActionRecord:
        world = cognitive_state.world
        agent = cognitive_state.agent

        config_state = world.get_object_state("config")
        dependency_state = world.get_object_state("dependency")
        service_state = world.get_object_state("service")

        latest_episode = episodic_memory.latest()
        if latest_episode and latest_episode.reflection.mismatch:
            semantic_memory.remember(
                "last_failure_reason",
                latest_episode.result.get("reason", "unknown_failure"),
            )

        remembered_failure_reason = semantic_memory.recall("last_failure_reason")

        if config_state != "valid":
            agent.current_hypothesis = "The service cannot recover until the configuration is valid."
            if remembered_failure_reason == "invalid_config":
                agent.current_strategy = "Use remembered mismatch evidence to repair configuration before retrying startup."
            else:
                agent.current_strategy = "Repair invalid configuration before attempting startup."
            agent.last_expected_outcome = "Configuration becomes valid and startup preconditions improve."
            return ActionRecord(
                name="fix_config",
                action_type="intervene",
                expected_outcome=agent.last_expected_outcome,
                rationale="Config is invalid and blocks successful service startup.",
            )

        if dependency_state != "installed":
            agent.current_hypothesis = "The missing dependency prevents the service from entering a running state."
            if remembered_failure_reason == "missing_dependency":
                agent.current_strategy = "Use remembered mismatch evidence to install the dependency before retrying startup."
            else:
                agent.current_strategy = "Install the missing dependency before startup."
            agent.last_expected_outcome = "Dependency becomes installed and service startup becomes feasible."
            return ActionRecord(
                name="install_dependency",
                action_type="intervene",
                expected_outcome=agent.last_expected_outcome,
                rationale="Dependency is missing and the service depends on it.",
            )

        if service_state != "running":
            agent.current_hypothesis = "All required preconditions are satisfied, so the service should start successfully."
            if remembered_failure_reason:
                agent.current_strategy = (
                    f"Retry startup while incorporating remembered failure signal: {remembered_failure_reason}."
                )
            else:
                agent.current_strategy = "Start the service after prerequisites are met."
            agent.last_expected_outcome = "Service reaches the running state."
            return ActionRecord(
                name="start_service",
                action_type="intervene",
                expected_outcome=agent.last_expected_outcome,
                rationale="Configuration and dependency states indicate startup should now succeed.",
            )

        agent.current_hypothesis = "The goal state has already been achieved."
        agent.current_strategy = "Preserve successful state and stop acting."
        agent.last_expected_outcome = "No further intervention is needed."
        return ActionRecord(
            name="inspect_service",
            action_type="observe",
            expected_outcome=agent.last_expected_outcome,
            rationale="Use a final observation step to confirm the stable goal state.",
        )
