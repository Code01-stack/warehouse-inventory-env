"""
Warehouse Inventory System - OpenEnv Environment
High-quality RL environment for warehouse management (submission-ready)
"""

from pydantic import BaseModel
from typing import Literal, List


# ---------------------------------------------------------------------------
# Data Models (OpenEnv compliant)
# ---------------------------------------------------------------------------

class WarehouseItem(BaseModel):
    item_name: str
    stock: int
    demand: int
    expiry_days: int


class WarehouseAction(BaseModel):
    action: Literal["restock", "prioritize_dispatch", "restock_and_dispatch"]
    item_name: str


class WarehouseObservation(BaseModel):
    task: str
    step: int
    items: List[WarehouseItem]


# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------

class WarehouseEnv:
    LOW_STOCK_THRESHOLD = 10
    EXPIRY_THRESHOLD = 3

    def __init__(self, task: Literal["easy", "medium", "hard"] = "easy"):
        self.task = task
        self.items: List[WarehouseItem] = []
        self.max_steps = 5
        self._step_count = 0

    # -----------------------------------------------------------------------
    # Reset
    # -----------------------------------------------------------------------
    def reset(self):
        self._step_count = 0

        # deterministic task setup
        if self.task == "easy":
            self.items = [
                WarehouseItem(item_name="Apples", stock=5, demand=3, expiry_days=10),
                WarehouseItem(item_name="Bananas", stock=50, demand=5, expiry_days=8),
                WarehouseItem(item_name="Carrots", stock=30, demand=4, expiry_days=12),
            ]

        elif self.task == "medium":
            self.items = [
                WarehouseItem(item_name="Milk", stock=40, demand=10, expiry_days=2),
                WarehouseItem(item_name="Bread", stock=25, demand=8, expiry_days=1),
                WarehouseItem(item_name="Cheese", stock=15, demand=3, expiry_days=7),
            ]

        elif self.task == "hard":
            self.items = [
                WarehouseItem(item_name="Rice", stock=8, demand=20, expiry_days=2),
                WarehouseItem(item_name="Pasta", stock=6, demand=15, expiry_days=3),
                WarehouseItem(item_name="Lentils", stock=50, demand=5, expiry_days=14),
            ]

        return {
            "observation": WarehouseObservation(**self.state()),
            "reward": 0.0,
            "done": False,
            "info": {}
        }

    # -----------------------------------------------------------------------
    # Step
    # -----------------------------------------------------------------------
    def step(self, action: WarehouseAction):
        self._step_count += 1

        item = self._find_item(action.item_name)

        if item is None:
            return {
                "observation": WarehouseObservation(**self.state()),
                "reward": 0.0,
                "done": False,
                "info": {"error": "Item not found"}
            }

        reward, info = self._apply_action(item, action.action)
        done = self._is_done()

        return {
            "observation": WarehouseObservation(**self.state()),
            "reward": reward,
            "done": done,
            "info": info
        }

    # -----------------------------------------------------------------------
    # State (required)
    # -----------------------------------------------------------------------
    def state(self):
        return {
            "task": self.task,
            "step": self._step_count,
            "items": [item.model_dump() for item in self.items],
        }

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------
    def _find_item(self, item_name):
        for item in self.items:
            if item.item_name == item_name:
                return item
        return None

    def _apply_action(self, item, action):
        reward = 0.0
        info = {}

        low_stock = item.stock < self.LOW_STOCK_THRESHOLD
        expiring = item.expiry_days <= self.EXPIRY_THRESHOLD
        high_demand = item.demand >= 10

        # ---------------- EASY ----------------
        if self.task == "easy":
            if action == "restock" and low_stock:
                item.stock += 30
                reward = 1.0
                info["message"] = "Restocked successfully"
            elif low_stock:
                reward = 0.3

        # ---------------- MEDIUM ----------------
        elif self.task == "medium":
            if action == "prioritize_dispatch" and expiring:
                item.expiry_days += 2
                item.stock -= item.demand
                reward = 1.0
                info["message"] = "Dispatched expiring item"
            elif expiring:
                reward = 0.3

        # ---------------- HARD ----------------
        elif self.task == "hard":
            if action == "restock_and_dispatch" and low_stock and expiring and high_demand:
                item.stock += 30
                item.stock -= item.demand
                item.expiry_days += 2
                reward = 1.0
                info["message"] = "Solved hard condition"
            elif low_stock or expiring:
                reward = 0.3

        return reward, info

    def _is_done(self):
        if self._step_count >= self.max_steps:
            return True

        for item in self.items:
            if item.stock < self.LOW_STOCK_THRESHOLD:
                return False
            if item.expiry_days <= self.EXPIRY_THRESHOLD:
                return False

        return True

    # -----------------------------------------------------------------------
    # Score (used by inference)
    # -----------------------------------------------------------------------
    def score(self):
        healthy = 0
        for item in self.items:
            if item.stock >= self.LOW_STOCK_THRESHOLD and item.expiry_days > self.EXPIRY_THRESHOLD:
                healthy += 1
        return round(healthy / len(self.items), 2)


# ---------------------------------------------------------------------------
# Task Graders (REQUIRED)
# ---------------------------------------------------------------------------

def grade_easy(env: WarehouseEnv) -> float:
    return env.score()

def grade_medium(env: WarehouseEnv) -> float:
    return env.score()

def grade_hard(env: WarehouseEnv) -> float:
    return env.score()


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    env = WarehouseEnv(task="easy")
    result = env.reset()

    print("Initial State:")
    print(result)

    first_item = result["observation"].items[0].item_name

    action = WarehouseAction(action="restock", item_name=first_item)
    result = env.step(action)

    print("\nAfter Action:")
    print(result)