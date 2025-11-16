"""Tests for policy engine."""
import pytest
from yaiy.policy import (
    PolicyEngine,
    PolicyRule,
    PolicyDecision,
    RiskLevel
)


def test_policy_engine_initialization():
    """Test policy engine initializes with default rules."""
    engine = PolicyEngine()
    assert len(engine.rules) > 0


def test_add_policy_rule():
    """Test adding custom policy rule."""
    engine = PolicyEngine()
    initial_count = len(engine.rules)
    
    rule = PolicyRule(
        name="test_rule",
        description="Test rule",
        risk_level=RiskLevel.LOW
    )
    engine.add_rule(rule)
    
    assert len(engine.rules) == initial_count + 1


def test_evaluate_requires_approval():
    """Test that evaluation requires approval by default."""
    engine = PolicyEngine()
    result = engine.evaluate("test_action", {})
    
    assert result.requires_approval is True
    assert result.decision in [PolicyDecision.REVIEW_REQUIRED, PolicyDecision.DENY]


def test_critical_risk_denied():
    """Test that critical risk actions are denied."""
    engine = PolicyEngine()
    
    # External communication is marked as critical
    result = engine.evaluate("external_communication", {"target": "internet"})
    
    assert result.risk_level == RiskLevel.CRITICAL or result.decision == PolicyDecision.DENY


def test_approve_action():
    """Test action approval recording."""
    engine = PolicyEngine()
    
    approval = engine.approve_action(
        "test_action",
        "human_operator",
        {"note": "approved for testing"}
    )
    
    assert approval["action"] == "test_action"
    assert approval["approver"] == "human_operator"
    assert approval["status"] == "approved"
    assert "timestamp" in approval


def test_policy_rule_evaluation():
    """Test individual policy rule evaluation."""
    rule = PolicyRule(
        name="test_rule",
        description="Test",
        risk_level=RiskLevel.MEDIUM,
        auto_approve=False
    )
    
    decision = rule.evaluate({})
    assert decision == PolicyDecision.REVIEW_REQUIRED


def test_high_risk_never_auto_approved():
    """Test that high risk rules never auto-approve."""
    rule = PolicyRule(
        name="test_high_risk",
        description="High risk test",
        risk_level=RiskLevel.HIGH,
        auto_approve=True  # Even with auto_approve, should require review
    )
    
    decision = rule.evaluate({})
    assert decision == PolicyDecision.REVIEW_REQUIRED
