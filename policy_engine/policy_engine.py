import json
from pathlib import Path
from typing import Dict, Any, List

class PolicyEngine:
    def __init__(self, ethics_spec_path: str = "ethics/ethics_spec.json"):
        self.ethics_spec = self._load_ethics_spec(ethics_spec_path)
        self.rules = self.ethics_spec.get("rules", [])
    
    def _load_ethics_spec(self, path: str) -> Dict[str, Any]:
        spec_path = Path(path)
        if not spec_path.exists():
            return {"rules": [], "version": "0.1.0"}
        with open(spec_path, 'r') as f:
            return json.load(f)
    
    def evaluate(self, action: Dict[str, Any]) -> Dict[str, Any]:
        violations = []
        approved = True
        
        for rule in self.rules:
            if not self._check_rule(action, rule):
                violations.append(rule.get("id", "unknown"))
                approved = False
        
        return {
            "approved": approved,
            "violations": violations,
            "action": action
        }
    
    def _check_rule(self, action: Dict[str, Any], rule: Dict[str, Any]) -> bool:
        rule_type = rule.get("type")
        
        if rule_type == "require_field":
            field = rule.get("field")
            return field in action
        elif rule_type == "no_network":
            return action.get("network_access", False) == False
        elif rule_type == "require_approval":
            return action.get("approved", False) == True
        
        return True
    
    def get_rules(self) -> List[Dict[str, Any]]:
        return self.rules

if __name__ == "__main__":
    engine = PolicyEngine()
    test_action = {"type": "forward", "network_access": False, "approved": True}
    result = engine.evaluate(test_action)
    print(f"Policy evaluation: {result}")
