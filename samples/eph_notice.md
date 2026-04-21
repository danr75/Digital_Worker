# Notice under s 118(1)(a1)
# Work Health and Safety Amendment (Digital Work Systems) Act 2026 (NSW)

**From:** [Entry permit holder]
**Entry permit number:** [permit number]
**Union:** [union]
**To:** [PCBU]
**Workplace:** [workplace address]
**Date:** [date]

---

## 1. Basis of notice

This notice is given under **section 118(1)(a1)** of the *Work Health and
Safety Act 2011* (NSW) as amended by the *Work Health and Safety Amendment
(Digital Work Systems) Act 2026* (NSW).

The entry permit holder suspects contraventions of:

- **s 19(3)(c1)** — Primary duty — failure to manage risks of digital work systems.
- **s 21A** — Specific duty relating to digital work systems.

## 2. Digital work system concerned

The digital work system concerned is the **Warehouse pick-rate — Western Sydney distribution centre**.

System type(s) identified (per the NSW AIAF alignment in these guidelines):

- Predictive ML system
- Rule-based automation

Sub-component(s) in focus for this notice:

- Pick-rate target-setting algorithm
- Wi-Fi location tracking and 'time off task' metric
- Supervisor dashboard (live ranking)

## 3. Grounds

The grounds on which the entry permit holder suspects contravention include:

- Complaints of sustained stress and inability to take toilet breaks.
- Pattern of older workers and pregnant workers disproportionately flagged as underperforming.
- Continuous location tracking via Wi-Fi triangulation from scanners.
- Dynamically rising pick-rate targets with no visible ceiling.

Risk types engaged under **s 21A(2)**:

- Excessive or unreasonable workloads
- Excessive or unreasonable performance metrics
- Excessive or unreasonable monitoring or surveillance
- Unlawful discriminatory practices or decision-making

## 4. Assistance requested

In accordance with s 118(1)(a1), the PCBU is requested to provide reasonable
assistance to access and inspect the digital work system. Specifically:

### 1. Pick-rate target-setting algorithm — source or business rules

- **Type:** code_and_logic
- **Proposed access mode:** vendor_walkthrough, code_review_under_nda, documentation_export
- **Proportionality notes:** Source code itself is rarely proportionate to request. A walkthrough of the business rules, input features, and how the target is computed will usually be sufficient.

- **Evidentiary value:** Establishes whether the target is set on a defensible basis and whether tenure, age, or pregnancy are used either directly or via proxy features.


### 2. Pick-rate target thresholds and ranking formulae

- **Type:** performance_metrics
- **Proposed access mode:** export, screen_share
- **Proportionality notes:** Proportionate to request the thresholds themselves and how they are derived (median, top quartile, rolling average, etc.). The numeric values are usually discoverable without IP concerns.

- **Evidentiary value:** Directly shows whether metrics are 'excessive or unreasonable' under s 21A(2)(b). Allows comparison against industry safe benchmarks.


### 3. Training data sample used to fit the target-setting model

- **Type:** training_data
- **Proposed access mode:** aggregated_export, data_room_inspection
- **Proportionality notes:** Full training data is rarely proportionate and carries high privacy risk. Aggregated statistics (feature distributions, per-cohort outcomes) are usually sufficient to test for discriminatory impact.

- **Evidentiary value:** Necessary to assess whether the model was trained on data skewed by demographic, tenure, or zone bias. Aggregated cohort statistics can establish disparate-impact grounds.


### 4. Manual target-override records

- **Type:** audit_trails
- **Proposed access mode:** export
- **Proportionality notes:** Proportionate to request de-identified override records. Individual records may engage privacy concerns.

- **Evidentiary value:** Shows whether human oversight is real (supervisors frequently override downward when a target is unreasonable) or absent.


### 5. Wi-Fi triangulation configuration (sampling rate, zones)

- **Type:** code_and_logic
- **Proposed access mode:** vendor_walkthrough, config_export
- **Proportionality notes:** Configuration (sampling rate, zones tracked, retention) is proportionate to request. Full firmware source is not.

- **Evidentiary value:** Establishes the intensity and scope of surveillance — key to s 21A(2)(c) and Workplace Surveillance Act analysis.


### 6. 'Time off task' and 'idle time' metric definitions

- **Type:** performance_metrics
- **Proposed access mode:** documentation_export, screen_share
- **Proportionality notes:** Proportionate to request the precise definitions, including what activities are excluded (breaks, rest, consultation with HSR).

- **Evidentiary value:** Shows whether the metric penalises lawful activity (toilet breaks, consultation under s 68, disability accommodations).


### 7. Worker location data logs (raw)

- **Type:** data_logs
- **Proposed access mode:** aggregated_export, data_room_inspection
- **Proportionality notes:** Raw location data is extremely sensitive. Aggregated or de-identified samples are usually proportionate; individual-level records only on specific grounds (e.g. a named complainant's consent).

- **Evidentiary value:** Establishes actual scope and intensity of surveillance in practice.


### 8. Surveillance notice issued under Workplace Surveillance Act 2005 (NSW)

- **Type:** records
- **Proposed access mode:** document_export
- **Proportionality notes:** Proportionate and usually volunteered by the PCBU; tests whether the surveillance was lawful in the first place.

- **Evidentiary value:** If no valid notice exists, the surveillance itself may be unlawful irrespective of s 21A.


### 9. Coaching-message triggering logic

- **Type:** code_and_logic
- **Proposed access mode:** vendor_walkthrough, config_export
- **Proportionality notes:** Proportionate to request the rules: when a message is sent, to whom, and what happens on repeated triggering (escalation path).

- **Evidentiary value:** Shows whether the escalation path itself amounts to unreasonable metrics or surveillance pressure.


### 10. Coaching messages sent to individual workers

- **Type:** records
- **Proposed access mode:** aggregated_export, sample_inspection
- **Proportionality notes:** Aggregated volumes (e.g. per-cohort) are proportionate; individual message contents only on consent or with de-identification.

- **Evidentiary value:** Demonstrates actual message cadence and tone. Relevant to psychosocial workload and to possible discriminatory patterns.


### 11. Coaching message templates / prompt templates

- **Type:** code_and_logic
- **Proposed access mode:** documentation_export
- **Proportionality notes:** Proportionate to request. If an LLM is used to generate messages, the prompt template and any safety guardrails are in scope.

- **Evidentiary value:** Shows whether message tone itself is pressuring or threatening, which bears on psychosocial workload.


### 12. Supervisor dashboard UI specification / wireframes

- **Type:** code_and_logic
- **Proposed access mode:** documentation_export, screen_share
- **Proportionality notes:** Proportionate to request a walkthrough of the fields shown, the ranking logic, and any colour-coding or flagging indicators.

- **Evidentiary value:** Shows what a supervisor sees live — which drives supervisor behaviour toward workers.


### 13. Supervisor dashboard access logs

- **Type:** data_logs
- **Proposed access mode:** aggregated_export
- **Proportionality notes:** Proportionate at aggregate level. Individual supervisor use patterns may raise privacy concerns.

- **Evidentiary value:** Shows how often and intensively supervisors consult the dashboard — relevant to whether the dashboard drives disproportionate intervention.


### 14. Historical ranking outputs per worker

- **Type:** records
- **Proposed access mode:** aggregated_export
- **Proportionality notes:** Aggregated by cohort (age band, tenure, pregnancy accommodation status) is proportionate; individual rankings only on named complaint.

- **Evidentiary value:** Essential for demonstrating disparate impact by age or pregnancy.


### 15. Change history for thresholds, ranking logic, and metrics

- **Type:** audit_trails
- **Proposed access mode:** export
- **Proportionality notes:** Proportionate to request. Change history frequently shows threshold creep not communicated to workers.

- **Evidentiary value:** Establishes whether thresholds have risen over time (the 'dynamically rising targets' sub-pattern).


### 16. Worker/HSR consultation records under s 47–49 WHS Act

- **Type:** human_oversight
- **Proposed access mode:** document_export
- **Proportionality notes:** Proportionate to request. Establishes whether consultation occurred before the system or its thresholds were changed.

- **Evidentiary value:** Relevant to primary duty compliance and to whether the employer has a defence based on consultation.


### 17. Supervisor-escalation records for underperformance

- **Type:** human_oversight
- **Proposed access mode:** aggregated_export, sample_inspection
- **Proportionality notes:** Aggregated by cohort is proportionate. Tests whether human oversight is applied consistently across workers.

- **Evidentiary value:** Shows whether human oversight in practice corrects or reinforces disparate impact.


### 18. Sample input/output traces for the target-setting algorithm

- **Type:** data_logs
- **Proposed access mode:** sample_inspection, data_room_inspection
- **Proportionality notes:** Proportionate if the walkthrough (wh_pick_rate_algo_source) is insufficient to establish how targets are actually computed in practice. De-identification is a precondition.

- **Evidentiary value:** Where source-code review is not proportionate, traces are the next best evidence of actual behaviour.



**Overall access mode requested:** both (inspect and explain)

## 5. Timing

s 118(2A) requires reasonable notice. For non-urgent matters, allow at least 24 hours; longer where artefacts require IT or vendor support to produce.

A response is sought by **[date — allow the period recommended above]**.

## 6. Other-law interactions acknowledged

The entry permit holder acknowledges the following other-law interactions,
which are raised for attention but not resolved by this notice:

- **Privacy Act 1988 (Cth) and Australian Privacy Principles** — Where the artefact contains personal information about workers, APPs apply. Consider de-identification, minimum-necessary access, and APP 11 security obligations. Specialist advice required.

- **Privacy and Personal Information Protection Act 1998 (NSW)** — PPIPA engages where the PCBU is (or is handling data on behalf of) a NSW public sector agency. Access and use must comply with the NSW IPPs. Specialist advice required.

- **Workplace Surveillance Act 2005 (NSW)** — Computer, camera, or tracking surveillance must be notified to workers and, in some cases, authorised. If no valid surveillance notice exists, the surveillance itself may be unlawful regardless of the s 21A analysis.

- **Legal professional privilege** — PCBU-held records may include privileged legal advice, particularly around audit trails and change records where legal was consulted. Privilege is not displaced by s 118(1)(a1).

- **Commercial-in-confidence and intellectual property** — Source code, model weights, and training data are typically subject to licensing or trade-secret protections. Proportionate access is usually a walkthrough under confidentiality undertakings rather than raw code.


Where an artefact is IP-sensitive or commercially confidential, the entry
permit holder is prepared to receive a walkthrough under reasonable
confidentiality undertakings rather than raw access to code or data.

## 7. Limits and exceptions

The entry permit holder recognises that the PCBU may properly withhold
information that is:

- subject to legal professional privilege;
- restricted by Commonwealth law under s 118(3);
- information that cannot reasonably be disclosed without breaching
  privacy obligations that have not been adequately mitigated (by
  de-identification, aggregation, or consent).

Where access is withheld on any of these grounds, the PCBU is asked to
specify the ground and to offer a proportionate alternative (e.g.
aggregated data, de-identified samples, or a walkthrough).

---

> **Disclaimer.** This document was produced by the Digital Work Systems Guidelines Prototype as **guidance, not legal advice**. The *Work Health and Safety Amendment (Digital Work Systems) Act 2026* (NSW) and any guidelines made under s 118A are the authoritative sources. Users should consult a lawyer or SafeWork NSW before taking regulatory action. The tool flags interactions with other legal regimes (Privacy Act 1988 (Cth), PPIPA, HRIPA, Workplace Surveillance Act 2005 (NSW), Fair Work Act 2009 (Cth), legal professional privilege, commercial confidence, or intellectual property) but does not resolve them.

