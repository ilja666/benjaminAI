from __future__ import annotations

import json
from pathlib import Path

from cacs.agent import CACSAgent
from cacs.environment import SandboxEnvironment


BASE_DIR = Path(__file__).resolve().parent
SCENARIO_PATH = BASE_DIR / "scenarios" / "service_recovery.json"
OUTPUT_DIR = BASE_DIR / "logs" / "latest_run"


def main() -> None:
    environment = SandboxEnvironment(SCENARIO_PATH)
    agent = CACSAgent(environment)
    result = agent.run(max_iterations=10)
    agent.save_artifacts(OUTPUT_DIR)
    (OUTPUT_DIR / "run_summary.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
