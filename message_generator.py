from typing import Dict, Any

def generate_message(action: str, category: str, merchant_id: str, merchant: Dict[str, Any], trigger: Dict[str, Any]) -> Dict[str, str]:
    """
    Generates a highly specific, compelling message tailored to the merchant's data and category.
    """
    
    rating = merchant.get("rating", "N/A")
    listing_score = merchant.get("listing_score", "N/A")
    
    # Format response rate
    response_rate = merchant.get("response_rate", "N/A")
    if isinstance(response_rate, float) and response_rate < 1.0:
        response_rate = int(response_rate * 100)
        
    last_active = merchant.get("last_active_days", "several")
    trigger_type = trigger.get("type", "activity")
    
    if action == "fix_rating":
        num_reviews = min(3, merchant.get("recent_reviews", 3))
        
        variants = [
            "Responding to a few recent reviews today can quickly rebuild customer trust.",
            "Addressing recent feedback now can improve how new customers perceive your business.",
            "Replying to recent customer reviews can help recover trust quickly."
        ]
        
        # Ensure deterministic selection based on merchant_id
        template_idx = sum(ord(c) for c in merchant_id) % len(variants)
        selected_template = variants[template_idx]
        
        if trigger_type == "spike":
            message = f"You’re getting higher visibility right now, but your {rating} rating can hold back new orders. {selected_template} Want me to draft those replies now?"
        else:
            message = f"Your rating dropped to {rating} — this can reduce new customer clicks. {selected_template} Want me to draft those replies now?"
    
    elif action == "improve_listing":
        message = f"Your listing score is stuck at {listing_score}. Missing details directly cause customers to choose other {category}s. Adding 2 high-quality photos instantly recovers lost clicks. Should I open the photo upload tool for you?"
        
    elif action == "run_campaign":
        trigger_val = trigger.get("value", trigger_type).title()
        message = f"You have no active offers while {trigger_val} traffic is high. With your {rating} rating, a ‘Flat 20% Off’ deal today can bring more walk-ins. Want me to create this offer now?"
        
    elif action == "enable_auto_reply":
        message = f"Your response rate is at {response_rate}%. Every missed message is a lost booking for your {category}. Turning on smart auto-replies locks in those customers instantly. Want me to enable the 1-click auto-responder?"
        
    elif action == "reactivate":
        message = f"Your {category} hasn't been active in {last_active} days. Inactive profiles get pushed down in local search results. A quick status update proves you are open and ready. Want me to draft a 2-sentence update right now?"
        
    elif action == "upsell":
        trigger_val = trigger.get("value", trigger_type).title()
        message = f"Your offer is already live and your {rating} rating gives you strong conversion potential. Boosting it today can increase visibility during {trigger_val} traffic. Want me to promote it now?"
        
    else:
        message = f"Let's boost your {category} performance today based on your {rating} rating. Want me to run an optimization scan?"

    return {
        "message": message,
        "cta": "yes_no",
        "suppression_key": f"{action}_{merchant_id}"
    }
