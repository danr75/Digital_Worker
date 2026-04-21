"""Other-law flags module (spec §6).

Surfaces — never resolves — interactions with other legal regimes. A flag
fires when its ``trigger_if_any`` matches the current session state
(selected system types, artefact types, or sensitivity flags from the
artefact registry).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from src.artefact_registry import ArtefactEntry

CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"
FLAGS_PATH = CONTENT_DIR / "other_law" / "flags.yaml"


@dataclass(frozen=True)
class OtherLawFlag:
    id: str
    name: str
    trigger_if_any: dict[str, list[str]]
    guidance: str
    hand_off_to: list[str]


def load_flags(path: Path = FLAGS_PATH) -> list[OtherLawFlag]:
    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return [
        OtherLawFlag(
            id=f["id"],
            name=f["name"],
            trigger_if_any=dict(f.get("trigger_if_any", {})),
            guidance=f["guidance"],
            hand_off_to=list(f.get("hand_off_to", [])),
        )
        for f in raw["flags"]
    ]


def _collect_sensitivity(artefacts: list[ArtefactEntry]) -> set[str]:
    out: set[str] = set()
    for a in artefacts:
        out.update(a.sensitivity_flags)
    return out


def active_flags(
    *,
    system_types: list[str],
    artefact_types: list[str],
    surfaced_artefacts: list[ArtefactEntry],
    flags: list[OtherLawFlag],
) -> list[OtherLawFlag]:
    """Return the subset of flags whose triggers match the session state."""
    sensitivity = _collect_sensitivity(surfaced_artefacts)
    active: list[OtherLawFlag] = []
    for flag in flags:
        triggers = flag.trigger_if_any
        matched = False
        if set(triggers.get("system_types", [])).intersection(system_types):
            matched = True
        if set(triggers.get("artefact_types", [])).intersection(artefact_types):
            matched = True
        if set(triggers.get("sensitivity_flags", [])).intersection(sensitivity):
            matched = True
        if matched:
            active.append(flag)
    return active


def flag_summary(flag: OtherLawFlag) -> dict[str, Any]:
    return {
        "id": flag.id,
        "name": flag.name,
        "guidance": flag.guidance,
        "hand_off_to": flag.hand_off_to,
    }
