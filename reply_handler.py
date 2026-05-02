from typing import Dict, Any

class ReplyHandler:
    @staticmethod
    def handle_reply(reply_data: Dict[str, Any]) -> Dict[str, Any]:
        text = reply_data.get("text", "").lower()
        
        # Deterministic simple NLP
        if any(word in text for word in ["yes", "interested", "more", "sure", "ok"]):
            return {"action": "send", "message": "Great! Here are more details about the offer."}
        elif any(word in text for word in ["no", "stop", "unsubscribe", "not"]):
            return {"action": "end", "message": "Understood. We will stop sending these."}
        else:
            return {"action": "wait"}
