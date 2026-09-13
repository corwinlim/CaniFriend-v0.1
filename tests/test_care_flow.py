import pytest
from agent.deterministic import plan_dinner_handoff
from agent.tools import approve_care_plan, accept_care_plan, complete_care_task, record_care_outcome, PLANS


def setup_function():
    PLANS.clear()


def test_recommends_trusted_available_carer():
    result = plan_dinner_handoff("pika")
    assert result["recommended_carer"]["carer_id"] == "neighbor-a"
    assert result["care_plan"]["requires_owner_approval"] is True


@pytest.mark.parametrize("alias", ["feed", "feeding", "dinner", "meal", "give dinner"])
def test_feeding_aliases_recommend_same_authorized_carer(alias):
    from agent.tools import find_trusted_carers
    assert find_trusted_carers("Pika", alias, "tonight")[0]["carer_id"] == "neighbor-a"


def test_unknown_task_is_rejected_not_silently_empty():
    from agent.tools import find_trusted_carers
    with pytest.raises(ValueError, match="Unsupported care task"):
        find_trusted_carers("pika", "medicate", "19:00")


def test_cannot_accept_before_owner_approval():
    result = plan_dinner_handoff("pika")
    with pytest.raises(PermissionError):
        accept_care_plan(result["care_plan"]["plan_id"], "neighbor-a")


def test_end_to_end_close_loop():
    result = plan_dinner_handoff("pika")
    plan_id = result["care_plan"]["plan_id"]
    approve_care_plan(plan_id, "owner-corwin", True)
    accept_care_plan(plan_id, "neighbor-a")
    completed = complete_care_task(plan_id, "photo://pika-dinner", "Pika looks normal")
    assert completed["status"] == "completed"
    event = record_care_outcome("pika", plan_id, "fed, water refreshed, condition normal")
    assert event["authoritative_store"] == "CAIOS"
