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


# ✅ ADD THIS PART
import uvicorn

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
