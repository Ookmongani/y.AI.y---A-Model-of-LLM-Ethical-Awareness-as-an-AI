"""
FastAPI Mediator Service for y.AI.y

Offline-first API service that mediates interactions with the ethical awareness system.
All operations require manual approval and are logged.
No external network access by default.
"""
from typing import Dict, Any, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from yaiy.policy import PolicyEngine, PolicyDecision
from yaiy.utils.canonical_json import canonicalize


app = FastAPI(
    title="y.AI.y Mediator",
    description="Secure Local-First LLM Ethical Awareness Mediator",
    version="0.1.0"
)

# Initialize policy engine
policy_engine = PolicyEngine()


class ActionRequest(BaseModel):
    """Request to perform an action."""
    action: str = Field(..., description="Action to perform")
    context: Dict[str, Any] = Field(default_factory=dict, description="Action context")
    requester: str = Field(..., description="Identity of requester")


class ActionResponse(BaseModel):
    """Response to action request."""
    decision: str
    risk_level: str
    rules_triggered: list
    reasoning: str
    timestamp: str
    requires_approval: bool


class ApprovalRequest(BaseModel):
    """Request to approve an action."""
    action: str
    approver: str
    context: Dict[str, Any] = Field(default_factory=dict)


class IngotRequest(BaseModel):
    """Request to validate an ingot."""
    data: Dict[str, Any]
    signature: Optional[str] = None
    public_key: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "y.AI.y Mediator",
        "version": "0.1.0",
        "status": "offline-first",
        "mode": "manual-approval-required"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "policy_engine": "active",
        "rules_loaded": len(policy_engine.rules)
    }


@app.post("/evaluate", response_model=ActionResponse)
async def evaluate_action(request: ActionRequest):
    """
    Evaluate an action against policies.
    
    All actions require manual approval by default.
    """
    evaluation = policy_engine.evaluate(request.action, request.context)
    
    return ActionResponse(
        decision=evaluation.decision.value,
        risk_level=evaluation.risk_level.value,
        rules_triggered=evaluation.rules_triggered,
        reasoning=evaluation.reasoning,
        timestamp=evaluation.timestamp,
        requires_approval=evaluation.requires_approval
    )


@app.post("/approve")
async def approve_action(request: ApprovalRequest):
    """
    Record manual approval for an action.
    
    This endpoint logs the approval but does NOT automatically execute the action.
    """
    approval = policy_engine.approve_action(
        request.action,
        request.approver,
        request.context
    )
    
    return {
        "status": "approval_recorded",
        "approval": approval,
        "note": "Approval recorded. Execute action separately with this approval token."
    }


@app.post("/validate-ingot")
async def validate_ingot(request: IngotRequest):
    """
    Validate an unsigned or signed ingot.
    
    Ingots are data packets that may contain model parameters or configurations.
    For production use, all ingots should be signed.
    """
    # Canonicalize the data
    canonical = canonicalize(request.data)
    
    # Check if signature provided
    if request.signature and request.public_key:
        # In production, verify signature here
        # For now, just validate structure
        return {
            "status": "signature_check_required",
            "canonical_hash": canonical,
            "note": "Use Ed25519 signer CLI to verify signature offline"
        }
    
    # Unsigned ingot warning
    return {
        "status": "unsigned_ingot",
        "canonical_hash": canonical,
        "warning": "Ingot is not signed. Sign before production use.",
        "data": request.data
    }


@app.get("/policies")
async def list_policies():
    """List all active policy rules."""
    return {
        "rules": [
            {
                "name": rule.name,
                "description": rule.description,
                "risk_level": rule.risk_level.value,
                "auto_approve": rule.auto_approve
            }
            for rule in policy_engine.rules
        ],
        "total": len(policy_engine.rules)
    }


@app.get("/offline-status")
async def offline_status():
    """
    Check offline operation status.
    
    This service is designed for offline-first operation.
    External network access should be disabled.
    """
    return {
        "mode": "offline-first",
        "external_network": "disabled",
        "manual_approval": "required",
        "auto_execution": "disabled",
        "note": "All operations require explicit human approval"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
