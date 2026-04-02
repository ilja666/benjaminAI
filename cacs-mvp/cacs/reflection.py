from __future__ import annotations

from .state import ReflectionRecord


class ReflectionEngine:
    def reflect(self, expectation: str | None, result: dict) -> ReflectionRecord:
        outcome = result.get("outcome", "unknown")
        goal_reached = result.get("goal_reached", False)
        reason = result.get("reason")

        explanation_parts: list[str] = []
        mismatch = False

        if expectation is None:
            explanation_parts.append("No explicit expectation was recorded before the action.")
        else:
            explanation_parts.append(f"Expected outcome: {expectation}")

        if outcome == "failure":
            mismatch = True
            explanation_parts.append("The action failed to produce the intended transition.")
            if reason:
                explanation_parts.append(f"Observed failure reason: {reason}.")
        elif outcome == "success" and not goal_reached and result.get("action") == "start_service":
            mismatch = True
            explanation_parts.append("The action succeeded locally but did not satisfy the full goal state.")
        else:
            explanation_parts.append(f"Observed outcome: {outcome}.")
            if goal_reached:
                explanation_parts.append("The goal state is now satisfied.")

        return ReflectionRecord(
            expectation=expectation or "No prior expectation recorded.",
            outcome=outcome,
            mismatch=mismatch,
            explanation=" ".join(explanation_parts),
        )
