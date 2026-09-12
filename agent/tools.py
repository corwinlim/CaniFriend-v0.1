from __future__ import annotations
from dataclasses import asdict
from shared.contracts import PetContext, CarerCandidate, CarePlan

PETS = {
    "pika": PetContext(
        pet_id="pika", name="Pika", species="dog", dinner="CaniBowl Chicken",
        amount_g=100, target_time="19:00",
        care_notes=("Refresh water", "Check general condition"),
    )
}

CARERS = [
    CarerCandidate("ace", "Ace", "family", False, "high", 12, 1.0, ("feed", "walk")),
    CarerCandidate("neighbor-a", "Neighbor A", "trusted neighbor", True, "high", 8, 1.0, ("feed",)),
    CarerCandidate("neighbor-b", "Neighbor B", "trusted neighbor", True, "medium", 3, 0.94, ("walk", "feed")),
]

PLANS: dict[str, CarePlan] = {}


def _normalize_pet_id(pet_id: str) -> str:
    key = pet_id.strip().lower()
    if key in PETS:
        return key
    for stored_id, pet in PETS.items():
        if pet.name.lower() == key:
            return stored_id
    raise KeyError(pet_id)


def get_pet_context(pet_id: str) -> dict:
    return asdict(PETS[_normalize_pet_id(pet_id)])


def find_trusted_carers(pet_id: str, task: str, time: str) -> list[dict]:
    del pet_id, time
    eligible = [c for c in CARERS if c.available and task in c.authorized_tasks]
    eligible.sort(key=lambda c: (c.familiarity == "high", c.completion_rate, c.previous_tasks), reverse=True)
    return [asdict(c) for c in eligible]


def create_care_plan(pet_id: str, task: str, candidate_id: str, target_time: str = "19:00") -> dict:
    pet_id = _normalize_pet_id(pet_id)
    plan = CarePlan(plan_id=f"plan-{pet_id}-{candidate_id}", pet_id=pet_id,
                    carer_id=candidate_id, task=task, target_time=target_time)
    PLANS[plan.plan_id] = plan
    return {**plan.public(), "requires_owner_approval": True}


def approve_care_plan(plan_id: str, owner_id: str, approved: bool) -> dict:
    if not owner_id:
        raise ValueError("owner_id is required")
    plan = PLANS[plan_id]
    if not approved:
        return {**plan.public(), "approved": False}
    plan.owner_approved = True
    plan.status = "approved"
    return {**plan.public(), "approved": True}


def accept_care_plan(plan_id: str, carer_id: str) -> dict:
    plan = PLANS[plan_id]
    if not plan.owner_approved:
        raise PermissionError("Owner approval required before acceptance")
    if plan.carer_id != carer_id:
        raise PermissionError("Carer mismatch")
    plan.accepted = True
    plan.status = "accepted"
    return plan.public()


def complete_care_task(plan_id: str, proof: str, observation: str) -> dict:
    plan = PLANS[plan_id]
    if not (plan.owner_approved and plan.accepted):
        raise PermissionError("Approved and accepted care plan required")
    plan.proof = proof
    plan.observation = observation
    plan.status = "completed"
    return plan.public()


def record_care_outcome(pet_id: str, plan_id: str, outcome: str) -> dict:
    plan = PLANS[plan_id]
    if plan.pet_id != pet_id or plan.status != "completed":
        raise ValueError("Only completed plans may be recorded")
    return {"event_type": "care.completed", "pet_id": pet_id, "plan_id": plan_id,
            "outcome": outcome, "authoritative_store": "CAIOS"}
