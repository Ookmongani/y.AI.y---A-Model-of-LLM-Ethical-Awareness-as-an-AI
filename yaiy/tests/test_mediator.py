"""Tests for FastAPI mediator."""
import pytest
from fastapi.testclient import TestClient

from yaiy.mediator import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns service info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "y.AI.y Mediator"
    assert data["status"] == "offline-first"


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_evaluate_action():
    """Test action evaluation endpoint."""
    request_data = {
        "action": "test_action",
        "context": {"test": "data"},
        "requester": "test_user"
    }
    
    response = client.post("/evaluate", json=request_data)
    assert response.status_code == 200
    data = response.json()
    
    assert "decision" in data
    assert "risk_level" in data
    assert data["requires_approval"] is True


def test_approve_action():
    """Test action approval endpoint."""
    request_data = {
        "action": "test_action",
        "approver": "human_operator",
        "context": {"note": "approved"}
    }
    
    response = client.post("/approve", json=request_data)
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "approval_recorded"
    assert "approval" in data


def test_validate_unsigned_ingot():
    """Test unsigned ingot validation."""
    request_data = {
        "data": {"test": "ingot", "version": "1.0"}
    }
    
    response = client.post("/validate-ingot", json=request_data)
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "unsigned_ingot"
    assert "warning" in data


def test_validate_signed_ingot():
    """Test signed ingot validation."""
    request_data = {
        "data": {"test": "ingot"},
        "signature": "fake_signature",
        "public_key": "fake_public_key"
    }
    
    response = client.post("/validate-ingot", json=request_data)
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "signature_check_required"


def test_list_policies():
    """Test listing policy rules."""
    response = client.get("/policies")
    assert response.status_code == 200
    data = response.json()
    
    assert "rules" in data
    assert data["total"] > 0


def test_offline_status():
    """Test offline status endpoint."""
    response = client.get("/offline-status")
    assert response.status_code == 200
    data = response.json()
    
    assert data["mode"] == "offline-first"
    assert data["external_network"] == "disabled"
    assert data["manual_approval"] == "required"
