"""Minimal structured audit events. Never log secrets, auth tokens, full health records, or photo bytes."""
from __future__ import annotations

import json
import logging
import time
import uuid
from typing import Any

logger = logging.getLogger("canifriend.audit")


def emit(event_type: str, **fields: Any) -> dict:
    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "timestamp_ms": int(time.time() * 1000),
        **fields,
    }
    logger.info(json.dumps(event, separators=(",", ":"), sort_keys=True))
    return event
