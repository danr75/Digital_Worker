"""Taxonomy loading and validation.

Loads the three reusable taxonomies (spec §3) from YAML. Each taxonomy is
loaded once at startup and used by the decision-tree engine, the artefact
registry, and the output templates.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"
TAXONOMY_DIR = CONTENT_DIR / "taxonomies"


@dataclass(frozen=True)
class TaxonomyEntry:
    id: str
    name: str
    data: dict[str, Any]


@dataclass(frozen=True)
class Taxonomy:
    taxonomy_id: str
    version: int
    source: list[str]
    entries: tuple[TaxonomyEntry, ...]

    def get(self, entry_id: str) -> TaxonomyEntry:
        for entry in self.entries:
            if entry.id == entry_id:
                return entry
        raise KeyError(f"No taxonomy entry with id={entry_id!r} in {self.taxonomy_id}")

    def ids(self) -> list[str]:
        return [entry.id for entry in self.entries]


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_taxonomy(path: Path) -> Taxonomy:
    raw = _load_yaml(path)
    entries = tuple(
        TaxonomyEntry(id=e["id"], name=e["name"], data=e) for e in raw["entries"]
    )
    return Taxonomy(
        taxonomy_id=raw["taxonomy_id"],
        version=raw["version"],
        source=list(raw.get("source", [])),
        entries=entries,
    )


def load_all_taxonomies(taxonomy_dir: Path = TAXONOMY_DIR) -> dict[str, Taxonomy]:
    return {
        path.stem: load_taxonomy(path)
        for path in sorted(taxonomy_dir.glob("*.yaml"))
    }
