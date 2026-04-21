"""Audit logging (spec §8).

Every user session is logged. Logs capture the structured traversal — role,
steps visited, selected tags, artefacts surfaced, flags raised — but
explicitly NOT the free-text user input (which may contain personal
information about workers). This is deliberate per spec §8.

Logs are written JSONL to ``audit_logs/`` (gitignored) with one file per
session. Aggregated usage data from these logs feeds the 12-month review
under s 276E.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LOG_DIR = Path(__file__).resolve().parent.parent / "audit_logs"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class AuditLogger:
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    log_dir: Path = field(default_factory=lambda: LOG_DIR)
    entries: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.log_dir.mkdir(parents=True, exist_ok=True)

    @property
    def path(self) -> Path:
        return self.log_dir / f"{self.session_id}.jsonl"

    def log(self, event: str, **payload: Any) -> None:
        entry = {
            "session_id": self.session_id,
            "ts": _now(),
            "event": event,
            **payload,
        }
        self.entries.append(entry)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def log_role(self, role_id: str) -> None:
        self.log("role_selected", role=role_id)

    def log_step(self, step_id: str, kind: str) -> None:
        self.log("step_visited", step_id=step_id, kind=kind)

    def log_answer(self, step_id: str, tags: list[str]) -> None:
        # NOTE: only structured tags; free text is never logged.
        self.log("answer_recorded", step_id=step_id, tags=list(tags))

    def log_artefacts(self, artefact_ids: list[str]) -> None:
        self.log("artefacts_surfaced", artefact_ids=list(artefact_ids))

    def log_flags(self, flag_ids: list[str]) -> None:
        self.log("other_law_flags_raised", flag_ids=list(flag_ids))

    def log_output(self, role_id: str, template: str, ai_assisted: bool) -> None:
        self.log(
            "output_rendered",
            role=role_id,
            template=template,
            ai_assisted=ai_assisted,
        )
