# Spec: Digital Work Systems Guidelines Prototype — Warehouse Pick-Rate Use Case (v1)

**Purpose:** a working prototype that supports interpretation and application of *Work Health and Safety Amendment (Digital Work Systems) Act 2026* (NSW) for a warehouse pick-rate scenario, designed so that its core components are reusable when subsequent use cases are added.

**Status:** draft for internal discussion. Not a commitment to build; intended to anchor conversations with the Office for AI, the AIRC secretariat, and any external specialist.

**Design principle for reusability:** separate the case-specific content (scenario narrative, concrete artefacts, worked examples) from the case-agnostic scaffolding (taxonomy, decision logic, artefact registry, role flows, governance). The scaffolding is designed once; the content is added per case. This document flags reusable components throughout with **[REUSABLE]** and case-specific content with **[CASE-SPECIFIC]**.

---

## 1. Scenario narrative [CASE-SPECIFIC]

A large distribution centre operating in Western Sydney employs around 1,200 workers on rotating shifts. Pickers use handheld barcode scanners linked to a warehouse management system that assigns each pick and displays a countdown timer derived from a dynamically-set target pick rate. The target rate is calculated by an algorithm drawing on historical pick data, worker tenure, zone, and time-of-day. Worker locations are tracked continuously via Wi-Fi triangulation from the scanners; a supervisor dashboard ranks workers live by pick rate, idle time, and "time off task." Workers falling below threshold receive automated coaching messages; repeated underperformance triggers escalation to a supervisor.

An entry permit holder has received complaints from workers about sustained stress, inability to take toilet breaks, and a pattern of older workers and pregnant workers being disproportionately flagged as underperforming. The EPH suspects contravention of s 19(3)(c1) and s 21A, and gives notice under s 118(1)(a1) requiring reasonable assistance to access and inspect the digital work system.

This scenario is anchored in evidence to the 2022 NSW Select Committee (Amazon Distribution Centre case study, Final Report Ch 2) and the inspectable-artefacts list in Minister Cotsis's Second Reading speech.

---

## 2. User roles [REUSABLE]

Four roles, used unchanged across all future use cases. Each has a distinct entry point, information need, and output.

- **WHS entry permit holder (EPH)** — preparing or issuing a s 118(1)(a1) notice; needs to frame a proportionate request and understand what "reasonable assistance" can be asked for.
- **PCBU representative** — receiving a notice; needs to understand what must be provided, what can be withheld, and how to document the response.
- **Health and safety representative / worker** — wanting to understand what the Act gives them visibility of, and how to raise concerns with EPH or inspectors.
- **SafeWork inspector** — exercising Part 9 powers in parallel; needs decision support on proportionate evidence requests.

The same role framework will apply across every future use case. Only the scenario content changes.

---

## 3. Taxonomy [REUSABLE]

This is the core reusable spine of the tool. Three aligned taxonomies, specified once, instantiated per case.

**3a. System-type taxonomy.** Aligned to s 4 definition and the NSW AIAF categories, so that a PCBU's existing AI Assessment Framework classification can be reused.

- Rule-based automation (deterministic logic, no learning)
- Predictive ML system (supervised or unsupervised learning)
- Generative AI (LLM-based or similar)
- Agentic AI (system that plans and takes actions)
- Online platform (two- or multi-sided marketplace)
- Hybrid (specify components)

**3b. Inspectable-artefact taxonomy.** Aligned directly to Minister Cotsis's Second Reading speech.

- Code and algorithmic logic (source code, business rules, model weights, configuration)
- Performance metrics (thresholds, targets, ranking logic, scoring formulae)
- Records (individual worker records, decision records, system-generated instructions)
- Data logs (access logs, system event logs, input/output logs)
- Audit trails (change history, override records, human-intervention records)
- Training data (for ML/AI systems — added to the Cotsis list because it's technically necessary)
- Human-oversight artefacts (human-in-the-loop records, escalation records, review decisions)

**3c. Risk-type taxonomy.** Directly from s 21A(2), unchanged.

- Excessive or unreasonable workloads
- Excessive or unreasonable performance metrics
- Excessive or unreasonable monitoring or surveillance
- Unlawful discriminatory practices or decision-making

---

## 4. Decision-tree logic [REUSABLE scaffolding, CASE-SPECIFIC branches]

**Outer layer (reusable across all cases):**

- Step 1 — Role identification and entry point
- Step 2 — Is this a digital work system as defined in s 4? (Taxonomy 3a)
- Step 3 — What s 21A(2) risks are being suspected? (Taxonomy 3c)
- Step 4 — What artefacts would be relevant? (Taxonomy 3b)
- Step 5 — What access mode is proportionate? (inspect / explain / both)
- Step 6 — What are the notice and timing constraints? (s 118(2A), s 117 note)
- Step 7 — What are the limits? (s 118(3), privilege, Commonwealth law, privacy, commercial confidentiality)
- Step 8 — Output: structured notice / structured response / structured investigation plan

**Rule encoding:** the decision logic is expressed as deterministic rules in a declarative YAML schema, not embedded in code. LLM components are kept out of decision logic entirely — they are used only for natural-language input parsing and natural-language output generation.

---

## 5. Artefact registry [REUSABLE scaffolding, CASE-SPECIFIC entries]

Schema for each entry: `artefact_id`, `artefact_name`, `artefact_type`, `typical_system_components`, `typical_access_methods`, `sensitivity_flags`, `proportionality_notes`, `evidentiary_value`, `related_risks`, `applicable_other_law`, `example_scenarios`.

---

## 6. Interaction-with-other-law module [REUSABLE]

- Privacy Act 1988 (Cth) and Australian Privacy Principles
- Privacy and Personal Information Protection Act 1998 (NSW)
- Health Records and Information Privacy Act 2002 (NSW)
- Workplace Surveillance Act 2005 (NSW)
- Fair Work Act 2009 (Cth)
- Commonwealth law override under s 118(3)
- Legal professional privilege
- Commercial-in-confidence and intellectual property
- Cross-border data-location issues

The tool never resolves these conflicts — it surfaces them as flags.

---

## 7. AI and non-AI components [REUSABLE]

**Deterministic components (no AI):** decision-tree execution, artefact-registry lookup, output-document generation from templates, role-based routing, audit logging.

**Assistive AI components (scoped LLM use):** natural-language input parsing, plain-language explanation of decision-tree branches, output drafting assistance. Human confirmation required before structured tags drive any output. Every AI-generated output is visibly marked and editable.

LLM components are explicitly *not* used for: determining what the Act requires, interpreting whether a risk exists, deciding what artefacts to request.

---

## 8. Governance [REUSABLE]

- AIAF assessment recorded and referred to AIRC (likely high-risk).
- Legal sign-off on decision logic, output templates, disclaimer framework, other-law handling.
- Consultation with Office for AI on AIAF alignment.
- Accessibility: WCAG 2.2 AA minimum.
- Audit logging: every user session logged.
- Disclaimer framework: every output labelled as guidance, not legal advice.

---

## 9. User flows [REUSABLE skeleton]

1. Role selection
2. Scenario framing
3. Decision-tree traversal
4. Artefact-registry surfacing
5. Other-law flag review
6. Output generation
7. Save / export / audit log

---

## 10. Out of scope (v1) [CASE-SPECIFIC]

- Other scenarios (food-delivery, ride-share, retail shift-offer, etc.) — v2+
- Dispute resolution under Part 7 Division 6 or s 142
- Inspector investigation planning under Part 9 (separate tool)
- Advice on s 19(3)(c1) duty compliance generally
- Automated advice outputs not reviewed by a human

---

## 11. Success criteria (v1)

- Three EPHs, three PCBU representatives, one AIRC member, one Office for AI representative review.
- Decision-tree traversal logs show no branch dead-ends or missing rules.
- Every output contains required disclaimers and references.

---

## 12. Reusable-artefacts register (summary)

**Build once:** roles (§2); taxonomies (§3); outer decision-tree (§4); artefact-registry schema (§5); other-law module (§6); AI/non-AI boundary (§7); governance (§8); user-flow skeleton (§9); success pattern (§11).

**Add per case:** scenario (§1); inner decision-tree branches (§4); artefact-registry entries (§5); case-specific other-law tuning (§6); case-specific prompts (§9); case-specific out-of-scope (§10); case-specific success measures (§11).

---

## 13. Build plan and team

- **Team:** policy lead, service designer, technologist, rules-engine specialist, digital-work-systems SME.
- **Timeline:** 12–14 weeks to consultation-ready prototype.
- **Platform:** Streamlit-class build; rules engine in YAML; thin frontend.
- **Budget principle:** invest in scaffolding first; content is cheaper to re-add than scaffolding is to retrofit.
