"""Role framework (spec §2).

Four reusable roles, each with a distinct entry point, information need, and
output. The same framework is used across all future cases.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Role:
    id: str
    name: str
    short_description: str
    entry_point: str
    information_need: str
    output_type: str


ROLES: tuple[Role, ...] = (
    Role(
        id="eph",
        name="WHS entry permit holder (EPH)",
        short_description=(
            "Union WHS entry permit holder preparing or issuing a s 118(1)(a1) "
            "notice."
        ),
        entry_point=(
            "I'm preparing a notice under s 118(1)(a1) that will ask a PCBU for "
            "reasonable assistance to access and inspect a digital work system."
        ),
        information_need=(
            "How do I frame a proportionate request? What artefacts can I ask "
            "for? What limits apply?"
        ),
        output_type="structured s 118(1)(a1) notice (draft)",
    ),
    Role(
        id="pcbu",
        name="PCBU representative",
        short_description=(
            "General counsel, HR leader, or WHS manager receiving a s 118(1)(a1) "
            "notice."
        ),
        entry_point=(
            "My organisation has received a notice under s 118(1)(a1) and I "
            "need to prepare a response."
        ),
        information_need=(
            "What must we provide? What can be withheld, and on what grounds? "
            "How do we document it?"
        ),
        output_type="structured response to s 118(1)(a1) notice (draft)",
    ),
    Role(
        id="hsr",
        name="Health and safety representative / worker",
        short_description=(
            "HSR or worker wanting to understand what visibility the Act gives "
            "them."
        ),
        entry_point=(
            "I want to understand what the Act lets me see about how my "
            "workplace's digital system affects me and my co-workers."
        ),
        information_need=(
            "What can I ask for? What can an EPH ask for on my behalf? How do "
            "I raise concerns?"
        ),
        output_type="plain-language orientation brief",
    ),
    Role(
        id="inspector",
        name="SafeWork inspector",
        short_description=(
            "SafeWork NSW inspector exercising Part 9 powers in parallel with "
            "an EPH process."
        ),
        entry_point=(
            "I'm planning an evidence request in an investigation that overlaps "
            "with an EPH inspection."
        ),
        information_need=(
            "What's proportionate to request under Part 9 given what the EPH "
            "can already see? How do I avoid duplicative or disproportionate "
            "demands?"
        ),
        output_type="proportionality check on evidence request",
    ),
)


def get_role(role_id: str) -> Role:
    for r in ROLES:
        if r.id == role_id:
            return r
    raise KeyError(f"Unknown role: {role_id!r}")


def role_ids() -> list[str]:
    return [r.id for r in ROLES]
