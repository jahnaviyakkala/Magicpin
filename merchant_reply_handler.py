from typing import Dict, Any

def handle_reply(reply_message: str, conversation_id: str, turn_number: int) -> Dict[str, str]:
    """
    Evaluates a merchant's reply to determine the conversational intent and exactly 
    what the system should do next (send, wait, or end).
    """
    
    # Normalize input for deterministic matching
    text = reply_message.lower().strip()
    
    # 1. Intent Detection Rules
    intent = "unknown"
    
    accept_keywords = ["yes", "do it", "sure", "ok", "okay", "proceed", "go ahead", "sounds good", "please", "yep"]
    reject_keywords = ["no", "not now", "later", "nah", "nope", "don't", "cancel"]
    clarify_keywords = ["what", "how", "explain", "why", "details", "more info", "meaning", "?"]
    hostile_keywords = ["stop", "irrelevant", "annoying", "spam", "unsubscribe", "shut up", "leave me alone", "bad"]
    
    # Matching sequence matters: Check hostile/clarify first, as a user might say "no wait, what does that mean?"
    if any(word in text.split() for word in hostile_keywords) or any(phrase in text for phrase in ["stop", "leave me alone"]):
        intent = "hostile"
    elif any(word in text.split() for word in clarify_keywords) or "?" in text:
        intent = "clarify"
    elif any(word in text.split() for word in reject_keywords) and not any(word in text.split() for word in accept_keywords):
        intent = "reject"
    elif any(word in text.split() for word in accept_keywords):
        intent = "accept"
        
    # 2. Determine Action and Response Body
    action = "wait"
    body = ""
    rationale = f"Detected intent: '{intent}' on turn {turn_number}."

    if intent == "accept":
        action = "send"
        # Confirm action + suggest next step
        body = "Great, I've started that process for you. Would you like me to send you a quick summary once it's finished?"
        rationale += " Proceeding with action and prompting for the next step."
        
    elif intent == "reject":
        action = "end"
        # Polite exit
        body = "Understood. We'll hold off for now. Have a great day!"
        rationale += " Ending conversation gracefully per rejection."
        
    elif intent == "clarify":
        action = "send"
        # Explain briefly + re-offer
        body = "This action optimizes your metrics to ensure you capture maximum local demand. Shall we go ahead and apply it?"
        rationale += " Providing brief context and re-offering the choice."
        
    elif intent == "hostile":
        action = "end"
        # De-escalate and end
        body = "I apologize for any inconvenience. I will stop messaging you now."
        rationale += " Immediate de-escalation and termination of the flow."
        
    else:  # unknown
        action = "wait"
        # Unknown -> wait (do not send a message)
        body = ""  
        rationale += " No clear intent recognized; pausing for human review or clearer input."

    return {
        "action": action,
        "body": body,
        "rationale": rationale
    }
