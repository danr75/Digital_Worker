"""Output rendering (spec §4 step 8, §9 step 6).

Renders role-specific output documents from Jinja2 templates in
``content/templates/``. Rendering is pure and deterministic; no LLM calls.
The optional ``ai_assisted`` flag controls only the presence of the
AI-assisted label, not the rendering itself.
"""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"
TEMPLATE_DIR = CONTENT_DIR / "templates"

STANDARD_DISCLAIMER = (
    "> **Disclaimer.** This document was produced by the Digital Work Systems "
    "Guidelines Prototype as **guidance, not legal advice**. The *Work Health "
    "and Safety Amendment (Digital Work Systems) Act 2026* (NSW) and any "
    "guidelines made under s 118A are the authoritative sources. Users should "
    "consult a lawyer or SafeWork NSW before taking regulatory action. The "
    "tool flags interactions with other legal regimes (Privacy Act 1988 "
    "(Cth), PPIPA, HRIPA, Workplace Surveillance Act 2005 (NSW), Fair Work "
    "Act 2009 (Cth), legal professional privilege, commercial confidence, or "
    "intellectual property) but does not resolve them."
)

AI_ASSISTED_LABEL = (
    "> **[AI-assisted draft — please review and edit before use.]**"
)


def _env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape(disabled_extensions=("md",)),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )


def render(template_name: str, context: dict) -> str:
    env = _env()
    template = env.get_template(template_name)
    ctx = dict(context)
    ctx.setdefault("standard_disclaimer", STANDARD_DISCLAIMER)
    ctx.setdefault("ai_assisted", False)
    ctx.setdefault("ai_assisted_label", AI_ASSISTED_LABEL)
    return template.render(**ctx)


def template_for_role(role_id: str) -> str:
    return {
        "eph": "eph_notice.md",
        "pcbu": "pcbu_response.md",
        "hsr": "hsr_brief.md",
        "inspector": "inspector_plan.md",
    }[role_id]
