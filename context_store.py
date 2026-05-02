from typing import Dict, Any, Optional

class ContextStore:
    def __init__(self):
        # schema: {scope: {context_id: {"version": int, "data": dict}}}
        self.store: Dict[str, Dict[str, Dict[str, Any]]] = {}

    def update_context(self, scope: str, context_id: str, version: int, data: Dict[str, Any]):
        if scope not in self.store:
            self.store[scope] = {}
            
        existing = self.store[scope].get(context_id)
        # Update only if version is strictly higher (or if it doesn't exist yet)
        if existing is None or version > existing["version"]:
            self.store[scope][context_id] = {
                "version": version,
                "data": data
            }

    def get_context(self, scope: str, context_id: str) -> Optional[Dict[str, Any]]:
        if scope in self.store and context_id in self.store[scope]:
            return self.store[scope][context_id]["data"]
        return None
        
    def get_all(self, scope: str) -> Dict[str, Dict[str, Any]]:
        if scope in self.store:
            return {k: v["data"] for k, v in self.store[scope].items()}
        return {}

    def get_counts(self) -> Dict[str, int]:
        return {scope: len(items) for scope, items in self.store.items()}

# Global singleton
store = ContextStore()
