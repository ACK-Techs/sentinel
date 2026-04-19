from __future__ import annotations

import importlib
import os
import random

from locust import HttpUser, LoadTestShape, between, task

scenario_module = importlib.import_module(f"scenarios.{os.getenv('SCENARIO', 'steady')}")
scenario = scenario_module.SCENARIO


class ScenarioShape(LoadTestShape):
    def tick(self):
        run_time = self.get_run_time()
        elapsed = 0
        for stage in scenario["stages"]:
            elapsed += stage["duration_s"]
            if run_time < elapsed:
                return stage["users"], stage["spawn_rate"]
        return None


class TargetUser(HttpUser):
    wait_time = between(0.1, 0.5)
    host = scenario["host"]

    @task
    def mixed_traffic(self) -> None:
        draw = random.randint(1, sum(scenario["endpoints"].values()))
        cumulative = 0
        for endpoint, weight in scenario["endpoints"].items():
            cumulative += weight
            if draw <= cumulative:
                method, path = endpoint.split(" ", 1)
                payload = {"sku": "SKU-001", "qty": 1, "amount": 25} if method == "POST" else None
                self.client.request(
                    method,
                    path,
                    name=endpoint,
                    headers={"X-Synthetic": "1"},
                    json=payload,
                    timeout=2.0,
                )
                return

