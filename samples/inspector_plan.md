# Proportionality check — evidence request plan
# Work Health and Safety Act 2011 (NSW), Part 9

**Prepared by:** [Inspector]
**Inspection number:** [number]
**Workplace:** [workplace]
**Date:** [date]

---

## 1. Context

This plan is generated to check the proportionality of an evidence request
under Part 9 of the WHS Act 2011 (NSW), in respect of the
**Warehouse pick-rate — Western Sydney distribution centre**.

Where an EPH is exercising s 118(1)(a1) in parallel, the plan below avoids
duplicative demands and documents the proportionality analysis for the
investigation file.

## 2. Digital work system identified

System type(s): Predictive ML system, Rule-based automation

Sub-component(s) in focus: Pick-rate target-setting algorithm, Wi-Fi location tracking and 'time off task' metric, Supervisor dashboard (live ranking)
## 3. Suspected risks (s 21A(2))

- Excessive or unreasonable workloads
- Excessive or unreasonable performance metrics
- Excessive or unreasonable monitoring or surveillance
- Unlawful discriminatory practices or decision-making

## 4. Proposed evidence requests

### 1. Pick-rate target-setting algorithm — source or business rules

- **Type:** code_and_logic
- **Access mode:** vendor_walkthrough, code_review_under_nda, documentation_export
- **Proportionality notes:** Source code itself is rarely proportionate to request. A walkthrough of the business rules, input features, and how the target is computed will usually be sufficient.

- **Evidentiary value for the investigation:** Establishes whether the target is set on a defensible basis and whether tenure, age, or pregnancy are used either directly or via proxy features.

- **EPH request overlap:** To confirm with EPH

### 2. Pick-rate target thresholds and ranking formulae

- **Type:** performance_metrics
- **Access mode:** export, screen_share
- **Proportionality notes:** Proportionate to request the thresholds themselves and how they are derived (median, top quartile, rolling average, etc.). The numeric values are usually discoverable without IP concerns.

- **Evidentiary value for the investigation:** Directly shows whether metrics are 'excessive or unreasonable' under s 21A(2)(b). Allows comparison against industry safe benchmarks.

- **EPH request overlap:** To confirm with EPH

### 3. Training data sample used to fit the target-setting model

- **Type:** training_data
- **Access mode:** aggregated_export, data_room_inspection
- **Proportionality notes:** Full training data is rarely proportionate and carries high privacy risk. Aggregated statistics (feature distributions, per-cohort outcomes) are usually sufficient to test for discriminatory impact.

- **Evidentiary value for the investigation:** Necessary to assess whether the model was trained on data skewed by demographic, tenure, or zone bias. Aggregated cohort statistics can establish disparate-impact grounds.

- **EPH request overlap:** To confirm with EPH

### 4. Manual target-override records

- **Type:** audit_trails
- **Access mode:** export
- **Proportionality notes:** Proportionate to request de-identified override records. Individual records may engage privacy concerns.

- **Evidentiary value for the investigation:** Shows whether human oversight is real (supervisors frequently override downward when a target is unreasonable) or absent.

- **EPH request overlap:** To confirm with EPH

### 5. Wi-Fi triangulation configuration (sampling rate, zones)

- **Type:** code_and_logic
- **Access mode:** vendor_walkthrough, config_export
- **Proportionality notes:** Configuration (sampling rate, zones tracked, retention) is proportionate to request. Full firmware source is not.

- **Evidentiary value for the investigation:** Establishes the intensity and scope of surveillance — key to s 21A(2)(c) and Workplace Surveillance Act analysis.

- **EPH request overlap:** To confirm with EPH

### 6. 'Time off task' and 'idle time' metric definitions

- **Type:** performance_metrics
- **Access mode:** documentation_export, screen_share
- **Proportionality notes:** Proportionate to request the precise definitions, including what activities are excluded (breaks, rest, consultation with HSR).

- **Evidentiary value for the investigation:** Shows whether the metric penalises lawful activity (toilet breaks, consultation under s 68, disability accommodations).

- **EPH request overlap:** To confirm with EPH

### 7. Worker location data logs (raw)

- **Type:** data_logs
- **Access mode:** aggregated_export, data_room_inspection
- **Proportionality notes:** Raw location data is extremely sensitive. Aggregated or de-identified samples are usually proportionate; individual-level records only on specific grounds (e.g. a named complainant's consent).

- **Evidentiary value for the investigation:** Establishes actual scope and intensity of surveillance in practice.

- **EPH request overlap:** To confirm with EPH

### 8. Surveillance notice issued under Workplace Surveillance Act 2005 (NSW)

- **Type:** records
- **Access mode:** document_export
- **Proportionality notes:** Proportionate and usually volunteered by the PCBU; tests whether the surveillance was lawful in the first place.

- **Evidentiary value for the investigation:** If no valid notice exists, the surveillance itself may be unlawful irrespective of s 21A.

- **EPH request overlap:** To confirm with EPH

### 9. Coaching-message triggering logic

- **Type:** code_and_logic
- **Access mode:** vendor_walkthrough, config_export
- **Proportionality notes:** Proportionate to request the rules: when a message is sent, to whom, and what happens on repeated triggering (escalation path).

- **Evidentiary value for the investigation:** Shows whether the escalation path itself amounts to unreasonable metrics or surveillance pressure.

- **EPH request overlap:** To confirm with EPH

### 10. Coaching messages sent to individual workers

- **Type:** records
- **Access mode:** aggregated_export, sample_inspection
- **Proportionality notes:** Aggregated volumes (e.g. per-cohort) are proportionate; individual message contents only on consent or with de-identification.

- **Evidentiary value for the investigation:** Demonstrates actual message cadence and tone. Relevant to psychosocial workload and to possible discriminatory patterns.

- **EPH request overlap:** To confirm with EPH

### 11. Coaching message templates / prompt templates

- **Type:** code_and_logic
- **Access mode:** documentation_export
- **Proportionality notes:** Proportionate to request. If an LLM is used to generate messages, the prompt template and any safety guardrails are in scope.

- **Evidentiary value for the investigation:** Shows whether message tone itself is pressuring or threatening, which bears on psychosocial workload.

- **EPH request overlap:** To confirm with EPH

### 12. Supervisor dashboard UI specification / wireframes

- **Type:** code_and_logic
- **Access mode:** documentation_export, screen_share
- **Proportionality notes:** Proportionate to request a walkthrough of the fields shown, the ranking logic, and any colour-coding or flagging indicators.

- **Evidentiary value for the investigation:** Shows what a supervisor sees live — which drives supervisor behaviour toward workers.

- **EPH request overlap:** To confirm with EPH

### 13. Supervisor dashboard access logs

- **Type:** data_logs
- **Access mode:** aggregated_export
- **Proportionality notes:** Proportionate at aggregate level. Individual supervisor use patterns may raise privacy concerns.

- **Evidentiary value for the investigation:** Shows how often and intensively supervisors consult the dashboard — relevant to whether the dashboard drives disproportionate intervention.

- **EPH request overlap:** To confirm with EPH

### 14. Historical ranking outputs per worker

- **Type:** records
- **Access mode:** aggregated_export
- **Proportionality notes:** Aggregated by cohort (age band, tenure, pregnancy accommodation status) is proportionate; individual rankings only on named complaint.

- **Evidentiary value for the investigation:** Essential for demonstrating disparate impact by age or pregnancy.

- **EPH request overlap:** To confirm with EPH

### 15. Change history for thresholds, ranking logic, and metrics

- **Type:** audit_trails
- **Access mode:** export
- **Proportionality notes:** Proportionate to request. Change history frequently shows threshold creep not communicated to workers.

- **Evidentiary value for the investigation:** Establishes whether thresholds have risen over time (the 'dynamically rising targets' sub-pattern).

- **EPH request overlap:** To confirm with EPH

### 16. Worker/HSR consultation records under s 47–49 WHS Act

- **Type:** human_oversight
- **Access mode:** document_export
- **Proportionality notes:** Proportionate to request. Establishes whether consultation occurred before the system or its thresholds were changed.

- **Evidentiary value for the investigation:** Relevant to primary duty compliance and to whether the employer has a defence based on consultation.

- **EPH request overlap:** To confirm with EPH

### 17. Supervisor-escalation records for underperformance

- **Type:** human_oversight
- **Access mode:** aggregated_export, sample_inspection
- **Proportionality notes:** Aggregated by cohort is proportionate. Tests whether human oversight is applied consistently across workers.

- **Evidentiary value for the investigation:** Shows whether human oversight in practice corrects or reinforces disparate impact.

- **EPH request overlap:** To confirm with EPH

### 18. Sample input/output traces for the target-setting algorithm

- **Type:** data_logs
- **Access mode:** sample_inspection, data_room_inspection
- **Proportionality notes:** Proportionate if the walkthrough (wh_pick_rate_algo_source) is insufficient to establish how targets are actually computed in practice. De-identification is a precondition.

- **Evidentiary value for the investigation:** Where source-code review is not proportionate, traces are the next best evidence of actual behaviour.

- **EPH request overlap:** To confirm with EPH


**Overall access mode:** both (inspect and explain)

## 5. Other-law interactions noted

- **Privacy Act 1988 (Cth) and Australian Privacy Principles** — Where the artefact contains personal information about workers, APPs apply. Consider de-identification, minimum-necessary access, and APP 11 security obligations. Specialist advice required.

- **Privacy and Personal Information Protection Act 1998 (NSW)** — PPIPA engages where the PCBU is (or is handling data on behalf of) a NSW public sector agency. Access and use must comply with the NSW IPPs. Specialist advice required.

- **Workplace Surveillance Act 2005 (NSW)** — Computer, camera, or tracking surveillance must be notified to workers and, in some cases, authorised. If no valid surveillance notice exists, the surveillance itself may be unlawful regardless of the s 21A analysis.

- **Legal professional privilege** — PCBU-held records may include privileged legal advice, particularly around audit trails and change records where legal was consulted. Privilege is not displaced by s 118(1)(a1).

- **Commercial-in-confidence and intellectual property** — Source code, model weights, and training data are typically subject to licensing or trade-secret protections. Proportionate access is usually a walkthrough under confidentiality undertakings rather than raw code.


## 6. Proportionality statement

The above requests have been generated by reference to the risk types and
sub-patterns selected. Before issuing, the inspector should confirm:

- No request duplicates an EPH request already underway (s 118(1)(a1)).
- For each request, the lowest-intrusion access mode sufficient to establish
  the evidentiary point has been chosen.
- De-identification or aggregation is applied wherever the evidentiary
  value is preserved at those levels.
- Where Commonwealth law or LPP could apply, the request is pre-scoped to
  avoid provoking a foreseeable objection.

---

> **Disclaimer.** This document was produced by the Digital Work Systems Guidelines Prototype as **guidance, not legal advice**. The *Work Health and Safety Amendment (Digital Work Systems) Act 2026* (NSW) and any guidelines made under s 118A are the authoritative sources. Users should consult a lawyer or SafeWork NSW before taking regulatory action. The tool flags interactions with other legal regimes (Privacy Act 1988 (Cth), PPIPA, HRIPA, Workplace Surveillance Act 2005 (NSW), Fair Work Act 2009 (Cth), legal professional privilege, commercial confidence, or intellectual property) but does not resolve them.

