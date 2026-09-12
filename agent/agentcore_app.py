"""CaniFriend Strands + Amazon Bedrock AgentCore entrypoint.

The LLM may understand the need, retrieve context, rank trusted carers, and
PROPOSE a care plan. Consequential state transitions remain actor-gated.
"""
from __future__ import annotations

import os
from typing import Any

from agent import tools as impl
from agent.audit import emit
from agent.deterministic import plan_dinner_handoff

SYSTEM_PROMPT = """You are CaniFriend, a trusted-neighborhood pet-care coordination agent.
Convert a pet owner's care need into a safe, auditable care proposal.

Rules:
1. Use tools to retrieve pet context and trusted carers; do not invent carers or feeding data.
2. Prefer already-authorized, available carers who are familiar with the pet.
3. You may CREATE a proposed care plan, but you MUST NEVER approve the handoff yourself.
4. Owner approval is a separate human action outside your toolset.
5. Disclose only minimum-necessary pet information.
6. If the request sounds medical, urgent, dangerous, or outside a carer's authorization, do not improvise; say escalation is required.
7. Keep the final answer concise and action-oriented for a mobile UI.
"""

DEFAULT_MODEL_ID = "amazon.nova-lite-v1:0"


def create_agent():
    from strands import Agent, tool
    from strands.models import BedrockModel

    @tool
    def get_pet_context(pet_id: str) -> dict:
        """Get minimum-necessary care context for one pet."""
        return impl.get_pet_context(pet_id)

    @tool
    def find_trusted_carers(pet_id: str, task: str, time: str) -> list[dict]:
        """Find available carers already authorized for this care task."""
        return impl.find_trusted_carers(pet_id, task, time)

    @tool
    def create_care_plan(pet_id: str, task: str, candidate_id: str, target_time: str) -> dict:
        """Create a PROPOSED care plan. Human owner approval is still required."""
        return impl.create_care_plan(pet_id, task, candidate_id, target_time)

    model = BedrockModel(
        model_id=os.getenv("CANIFRIEND_MODEL_ID", DEFAULT_MODEL_ID),
        region_name=os.getenv("AWS_REGION", "us-west-2"),
        temperature=0.1,
        max_tokens=700,
        streaming=False,
    )
    return Agent(model=model, system_prompt=SYSTEM_PROMPT,
                 tools=[get_pet_context, find_trusted_carers, create_care_plan])


def _serialize_agent_result(result: Any) -> str:
    message = getattr(result, "message", None)
    if isinstance(message, dict):
        chunks = message.get("content", [])
        texts = [c.get("text", "") for c in chunks if isinstance(c, dict) and c.get("text")]
        if texts:
            return "\n".join(texts)
    return str(result)


def handle_payload(payload: dict) -> dict:
    action = payload.get("action", "agent")
    request_id = payload.get("request_id") or "demo-request"
    emit("request.received", request_id=request_id, action=action)

    if action == "health":
        return {"ok": True, "service": "canifriend-agent", "version": "0.1.0"}

    if action == "agent":
        prompt = payload.get("prompt", "I can't get home tonight. Make sure Pika gets dinner.")
        mode = os.getenv("CANIFRIEND_AGENT_MODE", "strands").lower()
        if mode == "deterministic":
            response = {"mode": "deterministic", **plan_dinner_handoff(payload.get("pet_id", "pika"))}
            emit("care.proposed", request_id=request_id, mode="deterministic",
                 plan_id=response.get("care_plan", {}).get("plan_id"))
            return response
        agent = create_agent()
        started = __import__("time").perf_counter()
        result = agent(prompt)
        latency_ms = round((__import__("time").perf_counter() - started) * 1000)
        emit("agent.completed", request_id=request_id, mode="strands", latency_ms=latency_ms)
        return {"mode": "strands", "result": _serialize_agent_result(result), "latency_ms": latency_ms}

    if action == "approve":
        return impl.approve_care_plan(payload["plan_id"], payload["owner_id"], bool(payload.get("approved")))
    if action == "accept":
        return impl.accept_care_plan(payload["plan_id"], payload["carer_id"])
    if action == "complete":
        return impl.complete_care_task(payload["plan_id"], payload["proof"], payload.get("observation", ""))
    if action == "record_outcome":
        return impl.record_care_outcome(payload["pet_id"], payload["plan_id"], payload["outcome"])
    raise ValueError(f"Unsupported action: {action}")


def build_agentcore_app():
    from bedrock_agentcore.runtime import BedrockAgentCoreApp
    app = BedrockAgentCoreApp()

    @app.entrypoint
    def invoke(payload):
        try:
            return handle_payload(payload or {})
        except (KeyError, ValueError, PermissionError) as exc:
            return {"ok": False, "error": exc.__class__.__name__, "message": str(exc)}
    return app


if __name__ == "__main__":
    build_agentcore_app().run()
