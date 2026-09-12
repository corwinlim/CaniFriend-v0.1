from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Literal, Optional

CareStatus = Literal["proposed", "approved", "accepted", "completed"]

@dataclass(frozen=True)
class PetContext:
    pet_id: str
    name: str
    species: str
    dinner: str
    amount_g: int
    target_time: str
    care_notes: tuple[str, ...]

@dataclass(frozen=True)
class CarerCandidate:
    carer_id: str
    name: str
    relationship: str
    available: bool
    familiarity: Literal["low", "medium", "high"]
    previous_tasks: int
    completion_rate: float
    authorized_tasks: tuple[str, ...]

@dataclass
class CarePlan:
    plan_id: str
    pet_id: str
    carer_id: str
    task: str
    target_time: str
    status: CareStatus = "proposed"
    owner_approved: bool = False
    accepted: bool = False
    proof: Optional[str] = None
    observation: Optional[str] = None

    def public(self) -> dict:
        return asdict(self)
