"""Streamlit frontend (spec §9, §13).

Thin frontend — all decision logic lives in the rule engine, the artefact
registry, and the other-law module. This file only handles presentation,
state, and the user-flow skeleton.
"""

from __future__ import annotations

import streamlit as st

from src.audit import AuditLogger
from src.decision_tree import Session, resolve_next
from src.engine import (
    CaseBundle,
    EngineState,
    load_case,
    load_engine_state,
    run_artefact_lookup,
    run_compute_step,
    run_other_law_check,
    run_render_output,
)
from src.llm_assist import draft_grounds_paragraph, parse_scenario
from src.roles import ROLES, get_role

AVAILABLE_CASES = {"warehouse_pick_rate": "Warehouse pick-rate (Western Sydney)"}


# ---------------------------------------------------------------------------
# Streamlit state helpers
# ---------------------------------------------------------------------------

def _init_state() -> None:
    if "engine" not in st.session_state:
        st.session_state.engine = load_engine_state()
    if "case" not in st.session_state:
        st.session_state.case = load_case("warehouse_pick_rate")
    if "session" not in st.session_state:
        st.session_state.session = Session(
            current_step_id=st.session_state.case.ruleset.entry_step
        )
    if "logger" not in st.session_state:
        st.session_state.logger = AuditLogger()


def _reset() -> None:
    for key in ("engine", "case", "session", "logger"):
        st.session_state.pop(key, None)
    _init_state()


# ---------------------------------------------------------------------------
# UI: sidebar
# ---------------------------------------------------------------------------

def _sidebar() -> None:
    st.sidebar.title("Digital Work Systems Guidelines")
    st.sidebar.caption("v1 prototype — guidance, not legal advice")
    case_id = st.sidebar.selectbox(
        "Case",
        list(AVAILABLE_CASES),
        format_func=AVAILABLE_CASES.get,
    )
    if case_id != st.session_state.case.case_id:
        st.session_state.case = load_case(case_id)
        _reset()
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Session ID**")
    st.sidebar.code(st.session_state.logger.session_id)
    if st.sidebar.button("Restart session"):
        _reset()
        st.rerun()
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "**AI/non-AI boundary (spec §7)**\n\n"
        "Decision logic runs from YAML rules only. LLM help (where "
        "available) is scoped to parsing free-text and drafting narrative "
        "paragraphs, always human-reviewed."
    )


# ---------------------------------------------------------------------------
# UI: step renderers
# ---------------------------------------------------------------------------

def _render_role_step(session: Session) -> None:
    st.subheader("Step 1 — Role identification")
    role_options = {r.id: r for r in ROLES}
    choice = st.radio(
        "Who are you using the tool as today?",
        list(role_options),
        format_func=lambda rid: role_options[rid].name,
        index=None,
    )
    if choice:
        st.info(role_options[choice].entry_point)
        if st.button("Confirm role"):
            session.role = choice
            st.session_state.logger.log_role(choice)
            _advance(session)
            st.rerun()


def _render_multi_choice_step(session: Session, step) -> None:
    st.subheader(step.title)
    prompt = step.data.get("prompt", "")
    guidance = step.data.get("guidance", "")
    if guidance:
        st.caption(guidance)

    ref = step.data.get("ref_taxonomy")
    options = step.data.get("options")
    engine: EngineState = st.session_state.engine

    if ref:
        tax = engine.taxonomies[ref]
        labels = {e.id: e.name for e in tax.entries}
    elif options:
        labels = {o["id"]: o["name"] for o in options}
    else:
        labels = {}

    selected = st.multiselect(
        prompt,
        list(labels),
        format_func=labels.get,
    )
    min_select = int(step.data.get("min_select", 0))
    store_as = step.data.get("store_as") or {
        "step_2_system": "system_types",
        "step_3_risks": "risk_types",
        "step_4_artefacts": "artefact_types",
    }.get(step.id)

    if step.data.get("options"):
        with st.expander("Option details"):
            for o in step.data["options"]:
                st.markdown(f"**{o['name']}** — {o.get('description', '')}")

    if st.button("Confirm selection"):
        if len(selected) < min_select:
            st.warning(f"Select at least {min_select} option(s).")
            return
        if store_as:
            session.set(store_as, selected)
        st.session_state.logger.log_answer(step.id, selected)
        _advance(session)
        st.rerun()


def _render_automatic_steps(session: Session) -> None:
    """Run a chain of automatic steps until a user-input step or output."""
    case: CaseBundle = st.session_state.case
    engine: EngineState = st.session_state.engine

    surfaced_artefacts = []
    flags = []
    output_doc = None

    while session.current_step_id is not None:
        step = case.ruleset.get(session.current_step_id)
        session.history.append(step.id)
        st.session_state.logger.log_step(step.id, step.kind)

        if step.kind in (
            "role_selection",
            "multi_choice",
            "single_choice",
            "free_text_with_tags",
        ):
            break

        if step.kind == "compute":
            run_compute_step(step.data, session)
        elif step.kind == "artefact_lookup":
            surfaced_artefacts = run_artefact_lookup(
                step.data, session, engine, case.case_id
            )
            st.session_state.logger.log_artefacts(
                [a.artefact_id for a in surfaced_artefacts]
            )
        elif step.kind == "other_law_check":
            # Use the most recently surfaced artefacts if not yet populated.
            if not surfaced_artefacts:
                ids = session.get("surfaced_artefacts", []) or []
                surfaced_artefacts = [engine.registry.get(i) for i in ids]
            flags = run_other_law_check(
                step.data, session, engine, surfaced_artefacts
            )
            st.session_state.logger.log_flags([f.id for f in flags])
        elif step.kind == "render_output":
            if not surfaced_artefacts:
                ids = session.get("surfaced_artefacts", []) or []
                surfaced_artefacts = [engine.registry.get(i) for i in ids]
            if not flags:
                flag_ids = session.get("other_law_flag_ids", []) or []
                flags = [f for f in engine.other_law_flags if f.id in flag_ids]

            ai_assisted = bool(st.session_state.get("use_ai_draft"))
            extra: dict = {}
            if ai_assisted and session.role == "eph":
                extra["grounds"] = [
                    draft_grounds_paragraph(
                        session.get("warehouse_sub_patterns", []) or [],
                        session.get("warehouse_subcomponents", []) or [],
                    )
                ]
            output_doc = run_render_output(
                step.data,
                session,
                engine=engine,
                case=case,
                surfaced_artefacts=surfaced_artefacts,
                flags=flags,
                ai_assisted=ai_assisted,
                extra_context=extra,
            )
            st.session_state.logger.log_output(
                session.role or "unknown",
                step.data.get("template_map", {}).get(session.role, "?"),
                ai_assisted,
            )
            st.session_state["rendered_output"] = output_doc
        elif step.kind == "end":
            session.current_step_id = None
            break

        session.current_step_id = resolve_next(step, session)


def _advance(session: Session) -> None:
    case: CaseBundle = st.session_state.case
    step = case.ruleset.get(session.current_step_id)
    session.current_step_id = resolve_next(step, session)


# ---------------------------------------------------------------------------
# UI: output view
# ---------------------------------------------------------------------------

def _render_output_view() -> None:
    st.subheader("Generated output")
    doc = st.session_state.get("rendered_output")
    if doc is None:
        st.info("No output yet.")
        return
    st.download_button(
        "Download",
        data=doc,
        file_name="digital_work_systems_output.md",
        mime="text/markdown",
    )
    st.markdown(doc)


# ---------------------------------------------------------------------------
# UI: scaffolding info
# ---------------------------------------------------------------------------

def _render_scenario_framing() -> None:
    case: CaseBundle = st.session_state.case
    with st.expander("Scenario (case background)"):
        st.markdown(f"**{case.scenario.get('title', case.case_id)}**")
        st.caption(case.scenario.get("short_description", ""))
        st.markdown("**Suspected contraventions**")
        for c in case.scenario.get("suspected_contraventions", []):
            st.markdown(f"- {c['section']} — {c['description']}")
        st.markdown("**EPH grounds (as framed in the case)**")
        for g in case.scenario.get("eph_grounds", []):
            st.markdown(f"- {g}")


def _render_assist_toggle() -> None:
    with st.expander("AI-assist options (optional)"):
        st.markdown(
            "AI assistance is scoped (spec §7). It is not used for any "
            "decision the Act puts in front of a lawyer. Drafts produced "
            "with AI assistance are labelled in the output."
        )
        st.checkbox(
            "Draft the 'grounds' paragraph with AI assistance",
            key="use_ai_draft",
            value=bool(st.session_state.get("use_ai_draft", False)),
        )
        free_text = st.text_area(
            "Paste a free-text description of the system to get tag "
            "suggestions (offline fallback available)",
            key="scenario_free_text",
        )
        if st.button("Suggest tags"):
            engine = st.session_state.engine
            result = parse_scenario(
                free_text,
                system_taxonomy=engine.taxonomies["system_types"],
                risk_taxonomy=engine.taxonomies["risk_types"],
                artefact_taxonomy=engine.taxonomies["artefact_types"],
            )
            st.write("**Suggested system types:**", result.system_type_suggestions)
            st.write("**Suggested risks:**", result.risk_type_suggestions)
            st.write(
                "**Suggested artefact types:**", result.artefact_type_suggestions
            )
            st.caption(f"Source: {result.source}. {result.rationale}")
            st.info(
                "Suggestions are advisory. Please confirm each selection in "
                "the steps below."
            )


def _render_traversal_trace() -> None:
    with st.expander("Traversal trace (audit)"):
        session: Session = st.session_state.session
        st.code("\n".join(session.history) or "(none yet)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    st.set_page_config(page_title="Digital Work Systems Guidelines", layout="wide")
    _init_state()
    _sidebar()

    st.title("Digital Work Systems Guidelines Prototype")
    st.caption(
        "Guidance — not legal advice. See the disclaimer appended to every "
        "generated output."
    )

    _render_scenario_framing()
    _render_assist_toggle()

    session: Session = st.session_state.session
    case: CaseBundle = st.session_state.case

    _render_automatic_steps(session)

    if session.current_step_id is None:
        _render_output_view()
    else:
        step = case.ruleset.get(session.current_step_id)
        if step.kind == "role_selection":
            _render_role_step(session)
        elif step.kind == "multi_choice":
            _render_multi_choice_step(session, step)
        else:
            st.info(f"Step kind {step.kind!r} not yet implemented in the UI.")

    _render_traversal_trace()


if __name__ == "__main__":
    main()
