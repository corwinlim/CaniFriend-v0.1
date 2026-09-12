from datetime import UTC, datetime

from infra.bedrock_access_proof import DEFAULT_MAX_TOKENS, build_proof


def test_proof_is_redacted():
    proof = build_proof(
        identity={
            "Account": "123456789012",
            "Arn": "arn:aws:iam::123456789012:role/CaniFriend",
        },
        response={
            "ResponseMetadata": {"RequestId": "req-123", "HTTPStatusCode": 200},
            "stopReason": "end_turn",
            "usage": {"inputTokens": 10, "outputTokens": 2, "totalTokens": 12},
            "output": {"message": {"content": [{"text": "CANIFRIEND_BEDROCK_OK"}]}},
        },
        model_id="amazon.nova-lite-v1:0",
        region="us-west-2",
        latency_ms=42,
        now=datetime(2026, 9, 12, tzinfo=UTC),
    )

    assert proof["status"] == "PASS"
    assert proof["http_status"] == 200
    assert proof["request_id"] == "req-123"
    assert "Account" not in proof
    assert "Arn" not in proof
    assert "output" not in proof
    assert len(proof["principal_fingerprint"]) == 12
    assert proof["latency_ms"] == 42


def test_max_tokens_is_intentionally_small():
    assert DEFAULT_MAX_TOKENS == 16
