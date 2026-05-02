from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import time
from datetime import datetime

from context_store import store
from decision_engine import DecisionEngine
from merchant_reply_handler import handle_reply

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Magicpin AI Challenge Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
START_TIME = time.time()

# Link to the global store's internal dictionary to satisfy the user's exact logic
context_store = store.store

class ContextRequest(BaseModel):
    scope: str
    context_id: str
    version: int
    payload: Dict[str, Any]
    delivered_at: Optional[str] = None

class TickPayload(BaseModel):
    now: str
    available_triggers: List[Any]

class ReplyPayload(BaseModel):
    conversation_id: str
    message: str
    turn_number: Optional[int] = 1

@app.post("/v1/context")
def add_context(req: ContextRequest):
    # ensure scope exists
    if req.scope not in context_store:
        context_store[req.scope] = {}

    existing = context_store[req.scope].get(req.context_id)

    # version handling (important)
    if existing is None or req.version > existing["version"]:
        context_store[req.scope][req.context_id] = {
            "version": req.version,
            "data": req.payload
        }

    return {
        "accepted": True,
        "ack_id": f"ack_{req.scope}_{req.context_id}",
        "stored_at": datetime.utcnow().isoformat() + "Z"
    }

@app.post("/v1/tick")
def process_tick(req: TickPayload):
    # This plugs into DecisionEngine
    actions = DecisionEngine.process_tick(req.now, req.available_triggers)
    return {"actions": actions}

@app.post("/v1/reply")
def handle_reply_endpoint(req: ReplyPayload):
    # Deterministic reply handler
    action = handle_reply(req.message, req.conversation_id, req.turn_number)
    return action

@app.get("/")
def root():
    return {"message": "Magicpin bot is running"}

@app.get("/v1/healthz")
def healthz():
    uptime = time.time() - START_TIME
    counts = store.get_counts()
    return {
        "status": "healthy",
        "uptime_seconds": round(uptime, 2),
        "context_counts": counts
    }

@app.get("/v1/metadata")
def metadata():
    return {
        "team_name": "Magicpin AI Challengers",
        "team_members": ["Jahnavi", "Lokesh"],
        "model": "deterministic-rule-engine",
        "approach": "rule-based decision engine using merchant + trigger prioritization",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=1)
