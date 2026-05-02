from typing import List, Dict, Any
from context_store import store
from merchant_decision_engine import decide_best_action
from message_generator import generate_message

class DecisionEngine:
    @staticmethod
    def process_tick(now: str, available_triggers: List[Any]) -> List[Dict[str, Any]]:
        actions = []
        
        # Fetch data from Context Store (Prompt 1)
        merchants = store.get_all("merchant")
        
        # Sort to ensure deterministic output
        sorted_merchants = sorted(merchants.items(), key=lambda x: x[0])
        
        parsed_triggers = []
        for t in available_triggers:
            if isinstance(t, dict):
                trigger_id = t.get("trigger_id", "unknown")
                parsed_triggers.append((trigger_id, t))
            else:
                trigger_id = str(t)
                trigger_data = store.get_context("trigger", trigger_id) or {}
                parsed_triggers.append((trigger_id, trigger_data))
                
        sorted_triggers = sorted(parsed_triggers, key=lambda x: x[0])
        
        for trigger_id, trigger_data in sorted_triggers:
            for merchant_id, merchant_data in sorted_merchants:
                if len(actions) >= 20:
                    break
                    
                category = merchant_data.get("category", "restaurant")
                
                # 1. Decide best action (Prompt 2)
                best_action = decide_best_action(category, merchant_data, trigger_data)
                
                # 2. Generate message (Prompt 3)
                message_payload = generate_message(best_action, category, merchant_id, merchant_data, trigger_data)
                
                # 3. Formulate the final action payload for the /v1/tick endpoint
                action = {
                    "merchant_id": merchant_id,
                    "trigger_id": trigger_id,
                    "body": message_payload["message"],
                    "cta": message_payload["cta"],
                    "suppression_key": message_payload["suppression_key"]
                }
                actions.append(action)
                
            if len(actions) >= 20:
                break
                
        return actions
