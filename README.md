# Magicpin AI Challenge: Deterministic Engagement Engine

## 1. Overview
This is a high-performance, deterministic decision engine designed for merchant growth. Instead of relying on slow, unpredictable LLMs, this system uses a strict scoring matrix and deterministic templates to guarantee actionable, high-compulsion engagement. It evaluates merchant context, ranks intervention priorities, and generates tight, data-driven messages in less than a millisecond. 

## 2. Approach
The system is built on **FastAPI** as a lightweight, in-memory state engine. It exposes five primary endpoints:
- `POST /v1/context` - Ingests and stores merchant, category, and trigger states.
- `POST /v1/tick` - Evaluates the current state and triggers to generate optimal actions.
- `POST /v1/reply` - Handles conversational intent deterministically.
- `GET /v1/healthz` - Reports system uptime and context metrics.
- `GET /v1/metadata` - Exposes static team identity.

By eliminating external API calls, the system easily scales past 10 requests/sec with near-zero latency while entirely avoiding AI hallucinations.

## 3. Decision Logic
The core of the system is a weighted scoring engine that enforces strict conflict resolution. Marketing opportunities never override critical business health issues.

- **Critical Overrides**: 
  - Low Rating (< 3.5) → `fix_rating` (Maximum Priority)
  - Prolonged Inactivity (> 30 days) → `reactivate`
- **Trigger Routing**:
  - Spike → `upsell` (capitalizes on high visibility)
  - Festival + No Active Offer → `run_campaign`
  - Festival + Active Offer → `upsell/boost`
- **Health Indicators**:
  - Missing Photos / Details → `improve_listing`

## 4. Message Strategy
Messages are constructed using a tight, zero-fluff formula: **[Signal] + [Impact] + [Action] + [CTA]**. 

- **Data-Driven**: We inject exact, non-hallucinated merchant metrics (e.g., actual rating, active offers, category).
- **High Compulsion**: Messages avoid generic "marketing speak" (e.g., "capitalize on trends") in favor of specific outcomes (e.g., "convert profile views into walk-ins").
- **Single CTA**: Every message ends with exactly one clear, yes/no question.
- **Suppression**: A targeted `suppression_key` (e.g., `fix_rating_m_001`) prevents merchants from being spammed with identical actions.
- **Deterministic Variation**: Message copy rotates deterministically using a merchant ID hash, ensuring variety without randomness.

## 5. Reply Handling
The `POST /v1/reply` endpoint acts as a deterministic intent router using robust keyword sets:
- **Accept** (`yes`, `do it`) → Confirms action, suggests the next step, returns `send`.
- **Reject** (`no`, `not now`) → Triggers a polite exit, returns `end`.
- **Clarify** (`what`, `explain`) → Re-explains the value prop, re-offers the CTA, returns `send`.
- **Hostile** (`stop`, `unsubscribe`) → Instantly de-escalates and stops messaging, returns `end`.
- **Unknown** → Returns `wait` for human review or further input.

## 6. Tradeoffs
- **In-Memory Storage**: The current `context_store` relies on Python dictionaries. While incredibly fast and perfect for this latency constraint, production scaling would require migrating state to Redis or a structured database.
- **Rigid Intent Matching**: The reply handler uses strict keyword boundaries. While this guarantees 100% safety and determinism, it may misclassify highly nuanced human phrasing. 
- **Hardcoded Tone Mapping**: The system is highly optimized for specific verticals (`salon`, `restaurant`, `dentist`, `gym`). Expanding to unstructured edge-case categories requires manual template addition.

## 7. Deployment
**Live URL**: `<YOUR_URL>`

### Local Setup
```bash
pip install fastapi uvicorn pydantic
python main.py
```
