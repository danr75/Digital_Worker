"""Artefact registry (spec §5).

Reusable registry of every artefact the tool knows about, with standardised
fields. The schema is reusable across all cases; entries accumulate as cases
are added (spec §5 and §12).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"
ARTEFACT_DIR = CONTENT_DIR / "artefacts"

REQUIRED_FIELDS = {
    "artefact_id",
    "artefact_name",
    "artefact_type",
    "typical_system_components",
    "typical_access_methods",
    "sensitivity_flags",
    "proportionality_notes",
    "evidentiary_value",
    "related_risks",
    "applicable_other_law",
    "example_scenarios",
}


@dataclass(frozen=True)
class ArtefactEntry:
    artefact_id: str
    artefact_name: str
    artefact_type: str
    typical_system_components: list[str]
    typical_access_methods: list[str]
    sensitivity_flags: list[str]
    proportionality_notes: str
    evidentiary_value: str
    related_risks: list[str]
    applicable_other_law: list[str]
    example_scenarios: list[str]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ArtefactEntry":
        missing = REQUIRED_FIELDS - set(data)
        if missing:
            raise ValueError(
                f"Artefact {data.get('artefact_id', '?')!r} missing required "
                f"fields: {sorted(missing)}"
            )
        return cls(
            artefact_id=data["artefact_id"],
            artefact_name=data["artefact_name"],
            artefact_type=data["artefact_type"],
            typical_system_components=list(data["typical_system_components"]),
            typical_access_methods=list(data["typical_access_methods"]),
            sensitivity_flags=list(data["sensitivity_flags"]),
            proportionality_notes=data["proportionality_notes"],
            evidentiary_value=data["evidentiary_value"],
            related_risks=list(data["related_risks"]),
            applicable_other_law=list(data["applicable_other_law"]),
            example_scenarios=list(data["example_scenarios"]),
        )


@dataclass(frozen=True)
class ArtefactRegistry:
    entries: tuple[ArtefactEntry, ...]

    def all_ids(self) -> list[str]:
        return [e.artefact_id for e in self.entries]

    def get(self, artefact_id: str) -> ArtefactEntry:
        for e in self.entries:
            if e.artefact_id == artefact_id:
                return e
        raise KeyError(f"No artefact with id={artefact_id!r}")

    def filter_by_types(self, types: list[str]) -> list[ArtefactEntry]:
        return [e for e in self.entries if e.artefact_type in types]

    def filter_by_case(self, case_id: str) -> list[ArtefactEntry]:
        return [e for e in self.entries if case_id in e.example_scenarios]

    def filter_for_case_and_types(
        self, case_id: str, types: list[str]
    ) -> list[ArtefactEntry]:
        return [
            e
            for e in self.entries
            if case_id in e.example_scenarios and e.artefact_type in types
        ]


def load_registry(artefact_dir: Path = ARTEFACT_DIR) -> ArtefactRegistry:
    seen: dict[str, ArtefactEntry] = {}
    for path in sorted(artefact_dir.glob("*.yaml")):
        with path.open("r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)
        for entry_data in raw.get("entries", []):
            entry = ArtefactEntry.from_dict(entry_data)
            if entry.artefact_id in seen:
                # De-duplication (spec §5: "Duplicates are consolidated").
                existing = seen[entry.artefact_id]
                merged_scenarios = sorted(
                    set(existing.example_scenarios + entry.example_scenarios)
                )
                seen[entry.artefact_id] = ArtefactEntry(
                    artefact_id=existing.artefact_id,
                    artefact_name=existing.artefact_name,
                    artefact_type=existing.artefact_type,
                    typical_system_components=existing.typical_system_components,
                    typical_access_methods=existing.typical_access_methods,
                    sensitivity_flags=existing.sensitivity_flags,
                    proportionality_notes=existing.proportionality_notes,
                    evidentiary_value=existing.evidentiary_value,
                    related_risks=existing.related_risks,
                    applicable_other_law=existing.applicable_other_law,
                    example_scenarios=merged_scenarios,
                )
            else:
                seen[entry.artefact_id] = entry
    return ArtefactRegistry(entries=tuple(seen.values()))
