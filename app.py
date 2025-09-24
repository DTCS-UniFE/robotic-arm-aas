import json
import os
import time

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from redis import Redis

app = FastAPI(
    title="AAS - Robotic Arm",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

host = os.getenv("VALKEY_HOST", "localhost")
port = int(os.getenv("VALKEY_PORT", "6379"))
print(f"Trying Valkey connection at {host}:{port}")
redis_client = Redis(host=host, port=port, decode_responses=True)
print("Connected successfully to Valkey")
STATE_KEY = "robot_arm_state"

# Dati statici
static_data = {
    "asset_id": "RA-001",
    "type": "Robotic Arm",
    "manufacturer": "AAS Robotics Inc.",
    "model": "XR-21",
}

# Dynamic state format:
# dynamic_state = {
#    "position": [0, 0, 0],  # x, y, z
#    "status": "idle",  # idle | moving
# }


class MoveCommand(BaseModel):
    x: float = Field(..., ge=0.0, le=100.0)
    y: float = Field(..., ge=-50, le=50.0)
    z: float = Field(..., ge=0.0, le=100.0)


def load_state():
    state_json = redis_client.get(STATE_KEY)
    if state_json:
        print("Restoring state from DB")
        return json.loads(state_json)
    print("State not found in DB, fresh start...")
    return {"position": [0.0, 0.0, 0.0], "status": "idle"}


def save_state(state):
    redis_client.set(STATE_KEY, json.dumps(state))


# Initialize state: if it exists in the DB, it is restored from there,
# otherwise it is set to an initial value of {"position": [0.0, 0.0, 0.0], "status": "idle"}.
dynamic_state = load_state()


@app.get("/aas/static")
def get_static_info():
    return static_data


@app.get("/aas/state")
def get_dynamic_state():
    return dynamic_state


@app.post("/aas/move")
def move_robot_arm(cmd: MoveCommand):
    if dynamic_state["status"] == "moving":
        raise HTTPException(status_code=400, detail="Already moving")

    # Simulating robotic arm movement
    dynamic_state["status"] = "moving"
    save_state(dynamic_state)

    # Simulating some time for the robotic arm to fully move
    time.sleep(3)

    dynamic_state["position"] = [cmd.x, cmd.y, cmd.z]
    dynamic_state["status"] = "idle"
    save_state(dynamic_state)

    return {
        "message": "Moved to new position",
        "new_position": dynamic_state["position"],
    }
