# Governance

This document records the governance posture for v1 of the prototype.
Per §8 of the spec, the governance framework applies to the prototype as a
whole and does not re-trigger per case (unless a new case introduces material
new risks).

## AIAF (NSW AI Assessment Framework)

**Preliminary classification:** high-risk.

Reasons:
- Provides operational decision support to people who will act on it (EPHs
  framing notices, PCBUs responding, inspectors planning investigations).
- Outputs are used in a regulatory context (s 118(1)(a1) notices).
- Handles descriptions of systems that may process personal or sensitive
  information.

**Action:** formal AIAF assessment to be completed before any release beyond
internal review. Result to be referred to the AI Review Committee (AIRC).

## Legal sign-off

The following must be reviewed by Crown Solicitor's Office or SafeWork legal
before external release:

- Decision-tree logic in `content/rules/` (outer and inner layers).
- Output templates in `content/templates/`.
- Disclaimer framework in `docs/disclaimers.md`.
- Other-law handling in `content/other_law/flags.yaml`.

## Office for AI consultation

Alignment to be confirmed with the Office for AI on:

- System-type taxonomy (§3a) — consistency with AIAF categories.
- AI/non-AI boundary (§7) — consistency with NSW whole-of-government AI
  instruments.

## Accessibility

Target: WCAG 2.2 AA. The Streamlit frontend is a v1 choice; a GOV.AU
pattern-library implementation is the expected path to full accessibility
compliance before public release.

## Audit logging

Every user session is logged via `src/audit.py`. Logs include:

- Session ID, timestamp, selected role.
- Each decision-tree branch traversed.
- Each artefact surfaced.
- Each other-law flag raised.
- Final output produced (or abandoned).

Logs do **not** capture free-text user input that may contain personal
information about workers — the rule engine operates on structured tags only.
Aggregated usage data feeds the 12-month review under s 276E of the Act.

## Disclaimer framework

See `docs/disclaimers.md`. Every generated output includes the standard
disclaimer; every LLM-assisted draft is explicitly labelled as such.

## Re-referral triggers

An AIRC re-referral is required if:

- A new case introduces risk types not covered in §3c.
- The AI/non-AI boundary (§7) is changed to put an LLM inside any decision
  call.
- The tool begins producing outputs that are not reviewable by a human before
  action.
