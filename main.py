from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import time

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

class ContextPayload(BaseModel):
    scope: str
    context_id: str
    version: int
    payload: Dict[str, Any]

class TickPayload(BaseModel):
    now: str
    available_triggers: List[Any]

class ReplyPayload(BaseModel):
    conversation_id: str
    message: str
    turn_number: Optional[int] = 1

@app.post("/v1/context")
def update_context(req: ContextPayload):
    if req.scope not in ["merchant", "category", "customer", "trigger"]:
        raise HTTPException(status_code=400, detail="Invalid scope. Must be one of: merchant, category, customer, trigger")
        
    updated = store.update_context(
        req.scope, 
        req.context_id, 
        req.version, 
        req.payload
    )
    
    return {"success": True, "updated": updated}

@app.post("/v1/tick")
def process_tick(req: TickPayload):
    # This plugs into DecisionEngine which sequentially calls decide_best_action and generate_message
    actions = DecisionEngine.process_tick(req.now, req.available_triggers)
    return {"actions": actions}

@app.post("/v1/reply")
def handle_reply_endpoint(req: ReplyPayload):
    # This plugs directly into the deterministic reply handler
    action = handle_reply(req.message, req.conversation_id, req.turn_number)
    return action

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
        "version": "1.0.0",
        "description": "Deterministic engagement backend"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=1)
