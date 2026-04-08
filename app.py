from fastapi import FastAPI
from warehouse_env import WarehouseEnv, WarehouseAction

app = FastAPI()
env = WarehouseEnv()

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(action: dict):
    act = WarehouseAction(**action)
    return env.step(act)