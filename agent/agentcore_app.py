"""CaniFriend Strands + Amazon Bedrock AgentCore entrypoint."""
from __future__ import annotations

import os
import re
from typing import Any, Callable

from agent import tools as impl
from agent.audit import emit
from agent.deterministic import plan_dinner_handoff

SYSTEM_PROMPT = """You are CaniFriend, a trusted-neighborhood pet-care coordination agent.
Convert a pet owner's care need into a safe, auditable care proposal.

Rules:
1. Use tools to retrieve pet context and trusted carers; do not invent carers or feeding data.
2. Use the exact trusted pet_id supplied in REQUEST CONTEXT when calling tools.
3. Tool task values are canonical: use `feed` for feeding, dinner, or meal requests; use `walk` for walking.
4. Prefer already-authorized, available carers who are familiar with the pet.
5. You may CREATE a proposed care plan, but you MUST NEVER approve the handoff yourself.
6. Owner approval is a separate human action outside your toolset.
7. Disclose only minimum-necessary pet information.
8. If the request sounds medical, urgent, dangerous, or outside a carer's authorization, do not improvise; say escalation is required.
9. Keep the final answer concise and action-oriented for a mobile UI.
"""

DEFAULT_MODEL_ID = "amazon.nova-lite-v1:0"
THINKING_BLOCK = re.compile(r"<thinking>.*?</thinking>\s*", re.DOTALL | re.IGNORECASE)


def _audited_tool(name: str, call: Callable[..., Any], **kwargs: Any) -> Any:
    safe = {key: value for key, value in kwargs.items() if key in {"pet_id", "task", "candidate_id", "target_time"}}
    try:
        result = call(**kwargs)
        emit("tool.completed", tool=name, ok=True, result_count=len(result) if isinstance(result, list) else 1, **safe)
        return result
    except (KeyError, ValueError, PermissionError) as exc:
        emit("tool.completed", tool=name, ok=False, error_type=exc.__class__.__name__, **safe)
        raise


def create_agent():
    from strands import Agent, tool
    from strands.models import BedrockModel

    @tool
    def get_pet_context(pet_id: str) -> dict:
        """Get minimum-necessary care context for one pet using its exact trusted pet_id."""
        return _audited_tool("get_pet_context", impl.get_pet_context, pet_id=pet_id)

    @tool
    def find_trusted_carers(pet_id: str, task: str, time: str) -> list[dict]:
        """Find available authorized carers. task must be `feed` or `walk`."""
        return _audited_tool("find_trusted_carers", impl.find_trusted_carers, pet_id=pet_id, task=task, time=time)

    @tool
    def create_care_plan(pet_id: str, task: str, candidate_id: str, target_time: str) -> dict:
        """Create a PROPOSED care plan. task must be `feed` or `walk`; owner approval remains required."""
        return _audited_tool("create_care_plan", impl.create_care_plan, pet_id=pet_id, task=task, candidate_id=candidate_id, target_time=target_time)

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
            return THINKING_BLOCK.sub("", "\n".join(texts)).strip()
    return THINKING_BLOCK.sub("", str(result)).strip()


def _trusted_prompt(payload: dict, prompt: str) -> str:
    pet_id = impl._normalize_pet_id(str(payload.get("pet_id", "pika")))
    return f"REQUEST CONTEXT (trusted): pet_id={pet_id}; canonical_task=feed.\nOWNER REQUEST: {prompt}"


def handle_payload(payload: dict) -> dict:
    action = payload.get("action", "agent")
    request_id = payload.get("request_id") or "demo-request"
    emit("request.received", request_id=request_id, action=action)
    if action == "health":
        return {"ok": True, "service": "canifriend-agent", "version": "0.1.1"}
    if action == "agent":
        prompt = payload.get("prompt", "I can't get home tonight. Make sure Pika gets dinner.")
        mode = os.getenv("CANIFRIEND_AGENT_MODE", "strands").lower()
        if mode == "deterministic":
            response = {"mode": "deterministic", **plan_dinner_handoff(payload.get("pet_id", "pika"))}
            emit("care.proposed", request_id=request_id, mode="deterministic", plan_id=response.get("care_plan", {}).get("plan_id"))
            return response
        agent = create_agent()
        started = __import__("time").perf_counter()
        result = agent(_trusted_prompt(payload, prompt))
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
