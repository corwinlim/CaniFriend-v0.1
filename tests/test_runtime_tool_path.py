from agent.agentcore_app import _serialize_agent_result, _trusted_prompt


class FakeResult:
    message = {"content": [{"text": "<thinking>private chain</thinking>\nNeighbor A selected."}]}


def test_payload_pet_id_is_injected_as_trusted_context():
    prompt = _trusted_prompt({"pet_id": "Pika"}, "Please arrange dinner")
    assert "pet_id=pika" in prompt
    assert "canonical_task=feed" in prompt


def test_thinking_blocks_are_not_returned_to_client():
    output = _serialize_agent_result(FakeResult())
    assert "thinking" not in output
    assert output == "Neighbor A selected."
