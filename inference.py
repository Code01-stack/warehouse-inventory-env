import os
from openai import OpenAI
from warehouse_env import WarehouseEnv, WarehouseAction

# -----------------------------
# Config
# -----------------------------
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN", "dummy-key")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

# -----------------------------
# Init
# -----------------------------
env = WarehouseEnv()

MAX_STEPS = 5
rewards = []
steps_taken = 0

print(f"[START] task=warehouse env=warehouse_inventory_env model={MODEL_NAME}")

result = env.reset()

# -----------------------------
# Run loop
# -----------------------------
for step in range(1, MAX_STEPS + 1):
    obs = result["observation"]
    task = obs["task"]
    items = obs["items"]

    # -----------------------------
    # Smart item selection
    # -----------------------------
    selected_item = items[0]

    for it in items:
        if it["stock"] < 10 or it["expiry_days"] <= 3:
            selected_item = it
            break

    item = selected_item["item_name"]

    # -----------------------------
    # Smart action selection
    # -----------------------------
    if task == "easy":
        action_str = "restock"

    elif task == "medium":
        if selected_item["expiry_days"] <= 3:
            action_str = "prioritize_dispatch"
        else:
            action_str = "restock"

    else:  # hard
        if selected_item["stock"] < 10 and selected_item["expiry_days"] <= 3:
            action_str = "restock_and_dispatch"
        elif selected_item["stock"] < 10:
            action_str = "restock"
        else:
            action_str = "prioritize_dispatch"

    action = WarehouseAction(action=action_str, item_name=item)

    result = env.step(action)

    reward = result["reward"]
    done = result["done"]

    rewards.append(reward)
    steps_taken = step

    print(f"[STEP] step={step} action={action_str} reward={reward:.2f} done={str(done).lower()} error=null")

    if done:
        break

# -----------------------------
# Final score
# -----------------------------
score = env.score()
success = score >= 0.8

print(f"[END] success={str(success).lower()} steps={steps_taken} score={score:.2f} rewards={[round(r,2) for r in rewards]}")