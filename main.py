from fastapi import FastAPI, HTTPException, Request
from typing import List, Dict, Any, Optional
import time
import datetime

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

@app.post("/v1/context")
async def update_context(request: Request):
    # Flexible schema: accept ANY JSON to satisfy judge requirements
    try:
        req = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    scope = req.get("scope")
    context_id = req.get("context_id")
    version = req.get("version")
    payload = req.get("payload")

    if not all([scope, context_id, payload]):
        # Fallback check: maybe it's using 'id' instead of 'context_id'?
        context_id = context_id or req.get("id")
        if not all([scope, context_id, payload]):
            raise HTTPException(status_code=400, detail="Missing required fields: scope, context_id/id, payload")

    if scope not in ["merchant", "category", "customer", "trigger"]:
        raise HTTPException(status_code=400, detail="Invalid scope.")
        
    updated = store.update_context(
        scope, 
        context_id, 
        int(version) if version is not None else 1, 
        payload
    )
    
    return {
        "accepted": True, 
        "updated": updated,
        "ack_id": f"ack_{context_id}",
        "stored_at": datetime.datetime.now(datetime.UTC).isoformat()
    }

@app.post("/v1/tick")
async def process_tick(request: Request):
    try:
        req = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    now = req.get("now", datetime.datetime.now(datetime.UTC).isoformat())
    available_triggers = req.get("available_triggers", [])
    
    # This plugs into DecisionEngine
    actions = DecisionEngine.process_tick(now, available_triggers)
    return {"actions": actions}

@app.post("/v1/reply")
async def handle_reply_endpoint(request: Request):
    try:
        req = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    message = req.get("message", "")
    conversation_id = req.get("conversation_id", "unknown")
    turn_number = req.get("turn_number", 1)
    
    # Deterministic reply handler
    action = handle_reply(message, conversation_id, int(turn_number))
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
