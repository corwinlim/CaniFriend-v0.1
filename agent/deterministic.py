from __future__ import annotations
from agent.tools import get_pet_context, find_trusted_carers, create_care_plan


def plan_dinner_handoff(pet_id: str = "pika") -> dict:
    pet = get_pet_context(pet_id)
    candidates = find_trusted_carers(pet_id, "feed", pet["target_time"])
    if not candidates:
        return {"ok": False, "reason": "No trusted carer available", "pet": pet}
    best = candidates[0]
    plan = create_care_plan(pet_id, "feed", best["carer_id"], pet["target_time"])
    return {
        "ok": True,
        "pet": pet,
        "recommended_carer": best,
        "care_plan": plan,
        "reason": f"{best['name']} is available, authorized for feeding, familiar with {pet['name']}, and has completed {best['previous_tasks']} previous care tasks.",
    }
