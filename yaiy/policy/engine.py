"""
Lightweight Policy Engine for y.AI.y

Enforces ethical awareness policies with manual approval workflow.
All decisions require explicit human approval - no automatic approvals.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime


class PolicyDecision(Enum):
    """Policy decision outcomes."""
    APPROVE = "approve"
    DENY = "deny"
    REVIEW_REQUIRED = "review_required"
    PENDING = "pending"


class RiskLevel(Enum):
    """Risk assessment levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class PolicyRule:
    """A single policy rule."""
    name: str
    description: str
    risk_level: RiskLevel
    auto_approve: bool = False  # Default: always require manual approval
    
    def evaluate(self, context: Dict[str, Any]) -> PolicyDecision:
        """
        Evaluate rule against context.
        
        Args:
            context: Context data for evaluation
            
        Returns:
            PolicyDecision
        """
        # Default behavior: require review
        if not self.auto_approve:
            return PolicyDecision.REVIEW_REQUIRED
        
        # Even if auto-approve is enabled, high/critical risk requires review
        if self.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            return PolicyDecision.REVIEW_REQUIRED
        
        return PolicyDecision.PENDING


@dataclass
class PolicyEvaluation:
    """Result of policy evaluation."""
    decision: PolicyDecision
    risk_level: RiskLevel
    rules_triggered: List[str]
    reasoning: str
    timestamp: str
    requires_approval: bool


class PolicyEngine:
    """
    Lightweight policy engine with offline-first operation.
    
    All decisions default to requiring manual approval.
    No automatic approvals without explicit configuration.
    """
    
    def __init__(self):
        self.rules: List[PolicyRule] = []
        self._init_default_rules()
    
    def _init_default_rules(self):
        """Initialize default ethical awareness rules."""
        self.rules = [
            PolicyRule(
                name="data_access",
                description="Control access to sensitive data",
                risk_level=RiskLevel.HIGH
            ),
            PolicyRule(
                name="model_execution",
                description="Require approval for model inference",
                risk_level=RiskLevel.MEDIUM
            ),
            PolicyRule(
                name="external_communication",
                description="Block external network communication",
                risk_level=RiskLevel.CRITICAL
            ),
            PolicyRule(
                name="parameter_modification",
                description="Prevent unauthorized parameter changes",
                risk_level=RiskLevel.HIGH
            ),
            PolicyRule(
                name="ingot_signature",
                description="Verify all ingots are properly signed",
                risk_level=RiskLevel.CRITICAL
            ),
        ]
    
    def add_rule(self, rule: PolicyRule):
        """Add a new policy rule."""
        self.rules.append(rule)
    
    def evaluate(self, action: str, context: Dict[str, Any]) -> PolicyEvaluation:
        """
        Evaluate an action against all policies.
        
        Args:
            action: Action to evaluate
            context: Context data
            
        Returns:
            PolicyEvaluation with decision and reasoning
        """
        triggered_rules = []
        max_risk = RiskLevel.LOW
        
        # Evaluate all rules
        for rule in self.rules:
            decision = rule.evaluate(context)
            
            if decision != PolicyDecision.APPROVE:
                triggered_rules.append(rule.name)
                
                # Track highest risk level
                if self._risk_priority(rule.risk_level) > self._risk_priority(max_risk):
                    max_risk = rule.risk_level
        
        # Determine final decision
        if max_risk == RiskLevel.CRITICAL:
            final_decision = PolicyDecision.DENY
            reasoning = f"Critical risk detected. Action '{action}' blocked."
        elif triggered_rules:
            final_decision = PolicyDecision.REVIEW_REQUIRED
            reasoning = f"Action '{action}' requires manual approval. Triggered rules: {', '.join(triggered_rules)}"
        else:
            final_decision = PolicyDecision.REVIEW_REQUIRED
            reasoning = f"Default policy: manual approval required for '{action}'"
        
        return PolicyEvaluation(
            decision=final_decision,
            risk_level=max_risk,
            rules_triggered=triggered_rules,
            reasoning=reasoning,
            timestamp=datetime.utcnow().isoformat(),
            requires_approval=True  # Always require approval
        )
    
    def _risk_priority(self, level: RiskLevel) -> int:
        """Get priority value for risk level."""
        priorities = {
            RiskLevel.LOW: 1,
            RiskLevel.MEDIUM: 2,
            RiskLevel.HIGH: 3,
            RiskLevel.CRITICAL: 4
        }
        return priorities.get(level, 0)
    
    def approve_action(self, action: str, approver: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Record manual approval for an action.
        
        Args:
            action: Action being approved
            approver: Identity of approver
            context: Action context
            
        Returns:
            Approval record
        """
        return {
            "action": action,
            "approver": approver,
            "timestamp": datetime.utcnow().isoformat(),
            "context": context,
            "status": "approved"
        }
