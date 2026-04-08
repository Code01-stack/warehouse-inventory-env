from fastapi import FastAPI
from warehouse_env import WarehouseEnv, WarehouseAction

app = FastAPI()
env = WarehouseEnv()


@app.post("/reset")
def reset():
    return env.reset()


@app.post("/step")
def step(action: dict):
    act = WarehouseAction(**action)
    return env.step(act)


@app.get("/state")
def state():
    return env.state()