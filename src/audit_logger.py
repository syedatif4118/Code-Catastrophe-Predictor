"""
Autonomous Alpha - Audit Logger
Glass Box logging to JSONL for full system transparency.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from src.models import AuditLog


class AuditLogger:
    """
    Log all state transitions and reasoning to JSONL file.
    Provides complete Glass Box transparency.
    """

    def __init__(self, log_path: str):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log_transition(
        self,
        state: str,
        inputs: dict[str, Any],
        outputs: dict[str, Any],
        rationale: str,
        duration_ms: float = None,
    ):
        """
        Log a state machine transition.

        Args:
            state: Current state name
            inputs: Input data to this state
            outputs: Output data from this state
            rationale: Human-readable explanation
            duration_ms: Execution duration in milliseconds
        """
        audit_entry = AuditLog(
            timestamp=datetime.utcnow(),
            state=state,
            inputs=self._serialize(inputs),
            outputs=self._serialize(outputs),
            rationale=rationale,
            duration_ms=duration_ms,
        )

        # Append to JSONL file
        with open(self.log_path, 'a') as f:
            f.write(audit_entry.model_dump_json() + '\n')

    def _serialize(self, obj: Any) -> dict:
        """Serialize objects to JSON-compatible dict."""
        if hasattr(obj, 'model_dump'):
            # Pydantic model
            return obj.model_dump(mode='json')
        elif isinstance(obj, dict):
            return {k: self._serialize(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self._serialize(item) for item in obj]
        elif isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        else:
            return str(obj)
