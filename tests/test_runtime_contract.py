import os
import pytest

from agent.agentcore_app import handle_payload
from agent.tools import PLANS


def setup_function():
    PLANS.clear()
    os.environ["CANIFRIEND_AGENT_MODE"] = "deterministic"


def test_health_contract():
    health = handle_payload({"action": "health"})
    assert health["ok"] is True
    assert health["service"] == "canifriend-agent"


def test_agent_deterministic_fallback_proposes_not_approves():
    response = handle_payload({"action": "agent", "pet_id": "pika", "prompt": "I can't get home tonight. Make sure Pika gets dinner."})
    assert response["mode"] == "deterministic"
    assert response["care_plan"]["status"] == "proposed"
    assert response["care_plan"]["owner_approved"] is False


def test_state_transition_requires_human_approval():
    proposed = handle_payload({"action": "agent", "pet_id": "pika"})
    plan_id = proposed["care_plan"]["plan_id"]
    with pytest.raises(PermissionError):
        handle_payload({"action": "accept", "plan_id": plan_id, "carer_id": "neighbor-a"})
    approved = handle_payload({"action": "approve", "plan_id": plan_id, "owner_id": "owner-corwin", "approved": True})
    assert approved["status"] == "approved"
    accepted = handle_payload({"action": "accept", "plan_id": plan_id, "carer_id": "neighbor-a"})
    assert accepted["status"] == "accepted"


def test_complete_then_record_authoritative_caios_event():
    proposed = handle_payload({"action": "agent", "pet_id": "pika"})
    plan_id = proposed["care_plan"]["plan_id"]
    handle_payload({"action": "approve", "plan_id": plan_id, "owner_id": "owner-corwin", "approved": True})
    handle_payload({"action": "accept", "plan_id": plan_id, "carer_id": "neighbor-a"})
    completed = handle_payload({"action": "complete", "plan_id": plan_id, "proof": "photo://pika-dinner", "observation": "Pika looks normal"})
    assert completed["status"] == "completed"
    event = handle_payload({"action": "record_outcome", "pet_id": "pika", "plan_id": plan_id, "outcome": "fed, water refreshed, condition normal"})
    assert event["authoritative_store"] == "CAIOS"
