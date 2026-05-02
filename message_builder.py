from typing import Dict, Any

class MessageBuilder:
    @staticmethod
    def build_offer_message(merchant_data: Dict[str, Any], trigger_data: Dict[str, Any], customer_data: Dict[str, Any] = None) -> str:
        merchant_name = merchant_data.get("name", "our partner")
        offer_details = trigger_data.get("offer_details", "a special offer")
        return f"Hello! {merchant_name} has {offer_details} for you. Check it out!"
