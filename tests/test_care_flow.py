import pytest
from agent.deterministic import plan_dinner_handoff
from agent.tools import approve_care_plan, accept_care_plan, complete_care_task, record_care_outcome, PLANS


def setup_function():
    PLANS.clear()


def test_recommends_trusted_available_carer():
    result = plan_dinner_handoff("pika")
    assert result["ok"] is True
    assert result["recommended_carer"]["carer_id"] == "neighbor-a"
    assert result["care_plan"]["requires_owner_approval"] is True


def test_cannot_accept_before_owner_approval():
    result = plan_dinner_handoff("pika")
    plan_id = result["care_plan"]["plan_id"]
    with pytest.raises(PermissionError):
        accept_care_plan(plan_id, "neighbor-a")


def test_end_to_end_close_loop():
    result = plan_dinner_handoff("pika")
    plan_id = result["care_plan"]["plan_id"]
    approve_care_plan(plan_id, "owner-corwin", True)
    accept_care_plan(plan_id, "neighbor-a")
    completed = complete_care_task(plan_id, "photo://pika-dinner", "Pika looks normal")
    assert completed["status"] == "completed"
    event = record_care_outcome("pika", plan_id, "fed, water refreshed, condition normal")
    assert event["authoritative_store"] == "CAIOS"


def test_pet_name_normalizes_to_id():
    from agent.tools import get_pet_context
    assert get_pet_context("Pika")["pet_id"] == "pika"
