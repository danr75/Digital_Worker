"""Scoped LLM assistance (spec §7).

Three scoped jobs are permitted:

1. Natural-language input parsing — turn a free-text description of a
   system into suggested structured tags. Human confirmation is required
   before the tags drive any decision-tree step.
2. Plain-language explanation — generate a readable explanation of why a
   branch was taken. Always references the deterministic rule.
3. Output drafting assistance — produce a first-draft of a narrative field
   in an output document (e.g. the 'grounds' paragraph of a notice).

LLM components are explicitly **not** used for:

- Determining what the Act requires.
- Interpreting whether a risk exists.
- Deciding what artefacts to request.

v1 ships with a deterministic offline fallback for each job so the
prototype is usable without an API key. If an Anthropic API key is
configured (``ANTHROPIC_API_KEY``) and ``anthropic`` is importable, the
online path is used; otherwise the fallback.

Every output from this module is marked as AI-assisted by the caller.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from src.taxonomy import Taxonomy


@dataclass(frozen=True)
class ParseResult:
    system_type_suggestions: list[str]
    risk_type_suggestions: list[str]
    artefact_type_suggestions: list[str]
    rationale: str
    source: str  # "llm" or "fallback"


_KEYWORDS_SYSTEM = {
    "rule_based": ["rule-based", "deterministic", "no learning"],
    "predictive_ml": ["algorithm", "predictive", "machine learning", "ml ", "model"],
    "generative_ai": ["llm", "generative", "chatbot", "prompt"],
    "agentic_ai": ["agent", "autonomous", "plans", "takes actions"],
    "online_platform": ["platform", "marketplace", "gig", "dispatch"],
}
_KEYWORDS_RISK = {
    "unreasonable_workloads": [
        "workload", "pace", "countdown", "target", "quota", "stress", "fatigue",
    ],
    "unreasonable_metrics": [
        "metric", "threshold", "ranking", "score", "target", "kpi",
    ],
    "unreasonable_monitoring": [
        "surveillance", "monitoring", "tracking", "location", "camera",
        "time off task", "idle",
    ],
    "unlawful_discrimination": [
        "older", "age", "pregnant", "pregnancy", "disability", "discriminat",
    ],
}
_KEYWORDS_ARTEFACT = {
    "code_and_logic": ["code", "algorithm", "logic", "rule", "model"],
    "performance_metrics": ["threshold", "target", "metric", "ranking", "score"],
    "records": ["record", "message", "coaching", "individual"],
    "data_logs": ["log", "tracking data", "location data", "event"],
    "audit_trails": ["audit", "change history", "override"],
    "training_data": ["training data", "trained on"],
    "human_oversight": ["supervisor", "escalation", "review", "human"],
}


def _fallback_parse(text: str) -> ParseResult:
    t = text.lower()

    def match(mapping: dict[str, list[str]]) -> list[str]:
        return [k for k, kws in mapping.items() if any(kw in t for kw in kws)]

    return ParseResult(
        system_type_suggestions=match(_KEYWORDS_SYSTEM) or ["hybrid"],
        risk_type_suggestions=match(_KEYWORDS_RISK),
        artefact_type_suggestions=match(_KEYWORDS_ARTEFACT),
        rationale=(
            "Offline keyword match used — no LLM call made. Review all "
            "suggestions before confirming."
        ),
        source="fallback",
    )


def parse_scenario(
    text: str,
    *,
    system_taxonomy: Taxonomy | None = None,
    risk_taxonomy: Taxonomy | None = None,
    artefact_taxonomy: Taxonomy | None = None,
) -> ParseResult:
    """Parse free-text to tag suggestions. Always subject to human review."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return _fallback_parse(text)
    try:
        import anthropic  # type: ignore
    except ImportError:
        return _fallback_parse(text)

    client = anthropic.Anthropic(api_key=api_key)
    taxonomy_snippets: list[str] = []
    for tax, label in [
        (system_taxonomy, "system_types"),
        (risk_taxonomy, "risk_types"),
        (artefact_taxonomy, "artefact_types"),
    ]:
        if tax is not None:
            ids = ", ".join(tax.ids())
            taxonomy_snippets.append(f"{label}: [{ids}]")

    prompt = (
        "You are tagging a free-text description of a workplace digital "
        "system against three taxonomies. Return a JSON object with keys "
        "system_type_suggestions, risk_type_suggestions, "
        "artefact_type_suggestions (each a list of ids from the taxonomies "
        "below) and rationale (one short paragraph). Only suggest ids that "
        "appear in the taxonomies.\n\n"
        + "\n".join(taxonomy_snippets)
        + f"\n\nText:\n{text}"
    )
    try:
        resp = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=600,
            messages=[{"role": "user", "content": prompt}],
        )
        import json as _json

        raw = resp.content[0].text  # type: ignore[attr-defined]
        data: dict[str, Any] = _json.loads(raw)
        return ParseResult(
            system_type_suggestions=list(data.get("system_type_suggestions", [])),
            risk_type_suggestions=list(data.get("risk_type_suggestions", [])),
            artefact_type_suggestions=list(
                data.get("artefact_type_suggestions", [])
            ),
            rationale=data.get("rationale", ""),
            source="llm",
        )
    except Exception:
        return _fallback_parse(text)


def explain_branch(step_id: str, rule_summary: str, outcome: str) -> str:
    """Return a plain-language explanation. Always references the rule."""
    return (
        f"At {step_id}, the rule `{rule_summary}` applied, which led to "
        f"outcome: {outcome}. The rule is authored in YAML in "
        f"content/rules/ and is reviewable there."
    )


def draft_grounds_paragraph(
    sub_patterns: list[str], subcomponents: list[str]
) -> str:
    """Produce a first-draft narrative grounds paragraph.

    Offline fallback; callers should mark the result as AI-assisted.
    """
    if not sub_patterns and not subcomponents:
        return ""
    bits: list[str] = []
    if subcomponents:
        bits.append(
            "The entry permit holder's concerns focus on the "
            + ", ".join(s.replace("_", " ") for s in subcomponents)
            + "."
        )
    if sub_patterns:
        bits.append(
            "The suspected patterns include "
            + ", ".join(s.replace("_", " ") for s in sub_patterns)
            + "."
        )
    bits.append(
        "These patterns engage s 21A(2) and warrant a proportionate "
        "request for reasonable assistance under s 118(1)(a1)."
    )
    return " ".join(bits)
