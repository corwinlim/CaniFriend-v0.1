"""Produce a redacted, machine-readable proof of Bedrock access.

This script intentionally makes one small Converse request. It never prints the
prompt, model output, credentials, account ID, or caller ARN.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError

DEFAULT_MODEL_ID = "amazon.nova-lite-v1:0"
DEFAULT_REGION = "us-west-2"
DEFAULT_MAX_TOKENS = 16


def _fingerprint(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


def build_proof(
    *,
    identity: dict[str, Any],
    response: dict[str, Any],
    model_id: str,
    region: str,
    latency_ms: int,
    now: datetime | None = None,
) -> dict[str, Any]:
    metadata = response.get("ResponseMetadata", {})
    usage = response.get("usage", {})
    return {
        "schema": "canifriend.aws-bedrock-access-proof.v1",
        "status": "PASS",
        "checked_at": (now or datetime.now(UTC)).isoformat(),
        "region": region,
        "model_id": model_id,
        "principal_fingerprint": _fingerprint(identity["Arn"]),
        "account_fingerprint": _fingerprint(identity["Account"]),
        "request_id": metadata.get("RequestId"),
        "http_status": metadata.get("HTTPStatusCode"),
        "stop_reason": response.get("stopReason"),
        "usage": {
            "input_tokens": usage.get("inputTokens"),
            "output_tokens": usage.get("outputTokens"),
            "total_tokens": usage.get("totalTokens"),
        },
        "latency_ms": latency_ms,
    }


def main() -> int:
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or DEFAULT_REGION
    model_id = os.getenv("CANIFRIEND_MODEL_ID", DEFAULT_MODEL_ID)
    output_path = Path(
        os.getenv("CANIFRIEND_BEDROCK_PROOF_PATH", "artifacts/aws/bedrock-access-proof.json")
    )
    config = Config(retries={"max_attempts": 5, "mode": "adaptive"})
    try:
        sts_client = boto3.client("sts", region_name=region, config=config)
        bedrock_client = boto3.client("bedrock-runtime", region_name=region, config=config)
        identity = sts_client.get_caller_identity()
        started = time.perf_counter()
        response = bedrock_client.converse(
            modelId=model_id,
            messages=[
                {
                    "role": "user",
                    "content": [{"text": "Reply with exactly: CANIFRIEND_BEDROCK_OK"}],
                }
            ],
            inferenceConfig={"maxTokens": DEFAULT_MAX_TOKENS, "temperature": 0},
            requestMetadata={"application": "canifriend", "proof": "p1-a"},
        )
        proof = build_proof(
            identity=identity,
            response=response,
            model_id=model_id,
            region=region,
            latency_ms=round((time.perf_counter() - started) * 1000),
        )
    except (NoCredentialsError, ClientError, BotoCoreError) as exc:
        code = getattr(exc, "response", {}).get("Error", {}).get("Code", exc.__class__.__name__)
        print(json.dumps({"status": "FAIL", "error_code": code}), file=sys.stderr)
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(proof, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
