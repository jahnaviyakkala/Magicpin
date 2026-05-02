from typing import Dict, Any, Optional

def decide_best_action(category: str, merchant: Dict[str, Any], trigger: Dict[str, Any], customer: Optional[Dict[str, Any]] = None) -> str:
    """
    Deterministic decision engine for a merchant growth assistant.
    Evaluates merchant constraints and triggers to return exactly ONE best action.
    """
    
    # 1. Define fixed actions
    actions = [
        "fix_rating", 
        "improve_listing", 
        "run_campaign", 
        "enable_auto_reply", 
        "reactivate", 
        "upsell"
    ]
    
    # Initialize baseline scores
    scores = {action: 0 for action in actions}
    
    # Parse input signals with safe defaults
    rating = merchant.get("rating", 5.0)
    listing_score = merchant.get("listing_score", 100)
    response_rate = merchant.get("response_rate", 100)
    last_active_days = merchant.get("last_active_days", 0)
    offers = merchant.get("offers", 0)
    trigger_type = trigger.get("type", "none")
    
    # ---------------------------------------------------------
    # 2. Build Scoring System & Apply Conflict Resolutions
    # 
    # We assign scores to each action based on signals.
    # Conflict resolution is naturally handled by assigning 
    # overwhelming weights to critical constraints.
    # ---------------------------------------------------------

    # --- Conflict Resolution / Override Signals ---
    # If rating is poor, override all promotional actions
    if rating < 3.5:
        scores["fix_rating"] += 1000  # Highest priority override
        
    # If inactive, prioritize reactivation
    if last_active_days > 30:
        scores["reactivate"] += 800   # High priority override
        
    # If spike, prioritize upsell
    if trigger_type == "spike":
        scores["upsell"] += 600       # Priority override
        
    # --- Standard Signal Weights ---
    # Festival -> Medium priority unless major issue exists
    if trigger_type == "festival":
        if offers > 0:
            scores["upsell"] += 150
        else:
            scores["run_campaign"] += 100
    elif trigger_type == "dip":
        scores["run_campaign"] += 40
        scores["improve_listing"] += 30
    elif trigger_type == "recall":
        scores["run_campaign"] += 20
    elif trigger_type == "research":
        scores["improve_listing"] += 20
        
    # Merchant health signals
    if rating >= 3.5 and rating < 4.2:
        scores["fix_rating"] += 50    # Noticeable but not critical
        
    if listing_score < 60:
        scores["improve_listing"] += 70
    elif listing_score < 80:
        scores["improve_listing"] += 30
        
    if response_rate < 50:
        scores["enable_auto_reply"] += 70
    elif response_rate < 80:
        scores["enable_auto_reply"] += 30
        
    if offers == 0:
        scores["run_campaign"] += 40
        
    # Category modifiers
    if category in ["salon", "dentist", "pharmacy"]:
        # Time-sensitive/high-trust categories benefit heavily from auto-reply
        scores["enable_auto_reply"] += 15
    elif category in ["restaurant", "gym"]:
        # Volume-based categories benefit more from active campaigns
        scores["run_campaign"] += 15
        
    # 3. Deterministic Action Selection
    # Select best action: sort by score descending, then alphabetically by action name
    # This guarantees a single, predictable output every time
    best_action = max(scores.keys(), key=lambda action: (scores[action], action))
    
    return best_action
