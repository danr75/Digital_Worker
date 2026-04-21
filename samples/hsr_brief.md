# Orientation brief for HSRs and workers
# Work Health and Safety Amendment (Digital Work Systems) Act 2026 (NSW)

**Prepared for:** [HSR / worker]
**Workplace:** [workplace]
**Date:** [date]

---

## What this is

A plain-language brief explaining what the *Work Health and Safety Amendment
(Digital Work Systems) Act 2026* (NSW) lets you — and an entry permit holder
(EPH) acting for your union — ask about the **Warehouse pick-rate — Western Sydney distribution centre**.

## What the Act covers in this workplace

The system at your workplace is a **digital work system** under s 4 of the
Act. It uses the following kinds of technology:

- Predictive ML system
- Rule-based automation

## What risks the Act addresses (from s 21A(2))

- Excessive or unreasonable workloads
- Excessive or unreasonable performance metrics
- Excessive or unreasonable monitoring or surveillance
- Unlawful discriminatory practices or decision-making

### Patterns identified in this workplace

- Pace-forcing via countdown timer
- Dynamically rising targets with no ceiling
- Continuous location tracking
- Disparate impact by age or pregnancy
- Thresholds not disclosed to workers

## What can be looked at

An EPH can ask for "reasonable assistance" under s 118(1)(a1) to look at
parts of the digital work system. For the sub-component(s) in focus here,
the tool has identified the following kinds of artefact as relevant:

- **Pick-rate target-setting algorithm — source or business rules** — Establishes whether the target is set on a defensible basis and whether tenure, age, or pregnancy are used either directly or via proxy features.

- **Pick-rate target thresholds and ranking formulae** — Directly shows whether metrics are 'excessive or unreasonable' under s 21A(2)(b). Allows comparison against industry safe benchmarks.

- **Training data sample used to fit the target-setting model** — Necessary to assess whether the model was trained on data skewed by demographic, tenure, or zone bias. Aggregated cohort statistics can establish disparate-impact grounds.

- **Manual target-override records** — Shows whether human oversight is real (supervisors frequently override downward when a target is unreasonable) or absent.

- **Wi-Fi triangulation configuration (sampling rate, zones)** — Establishes the intensity and scope of surveillance — key to s 21A(2)(c) and Workplace Surveillance Act analysis.

- **'Time off task' and 'idle time' metric definitions** — Shows whether the metric penalises lawful activity (toilet breaks, consultation under s 68, disability accommodations).

- **Worker location data logs (raw)** — Establishes actual scope and intensity of surveillance in practice.

- **Surveillance notice issued under Workplace Surveillance Act 2005 (NSW)** — If no valid notice exists, the surveillance itself may be unlawful irrespective of s 21A.

- **Coaching-message triggering logic** — Shows whether the escalation path itself amounts to unreasonable metrics or surveillance pressure.

- **Coaching messages sent to individual workers** — Demonstrates actual message cadence and tone. Relevant to psychosocial workload and to possible discriminatory patterns.

- **Coaching message templates / prompt templates** — Shows whether message tone itself is pressuring or threatening, which bears on psychosocial workload.

- **Supervisor dashboard UI specification / wireframes** — Shows what a supervisor sees live — which drives supervisor behaviour toward workers.

- **Supervisor dashboard access logs** — Shows how often and intensively supervisors consult the dashboard — relevant to whether the dashboard drives disproportionate intervention.

- **Historical ranking outputs per worker** — Essential for demonstrating disparate impact by age or pregnancy.

- **Change history for thresholds, ranking logic, and metrics** — Establishes whether thresholds have risen over time (the 'dynamically rising targets' sub-pattern).

- **Worker/HSR consultation records under s 47–49 WHS Act** — Relevant to primary duty compliance and to whether the employer has a defence based on consultation.

- **Supervisor-escalation records for underperformance** — Shows whether human oversight in practice corrects or reinforces disparate impact.

- **Sample input/output traces for the target-setting algorithm** — Where source-code review is not proportionate, traces are the next best evidence of actual behaviour.


Not all of these are always available in full — some are subject to
confidentiality, privacy, or intellectual-property constraints. The tool
raises these as flags rather than resolving them.

## How to raise a concern

1. **Talk to your HSR** if you have one. The HSR can raise concerns through
   the consultation process (s 47–49 of the WHS Act).
2. **Ask an EPH** from your union to consider a s 118(1)(a1) notice if the
   concerns are about the digital work system.
3. **Report to SafeWork NSW** if you believe there is a serious or
   immediate risk.

## What this brief is not

This brief is general orientation only. It is not legal advice and does not
give you power to require access to the system yourself — an EPH or a
SafeWork inspector must do that.

---

> **Disclaimer.** This document was produced by the Digital Work Systems Guidelines Prototype as **guidance, not legal advice**. The *Work Health and Safety Amendment (Digital Work Systems) Act 2026* (NSW) and any guidelines made under s 118A are the authoritative sources. Users should consult a lawyer or SafeWork NSW before taking regulatory action. The tool flags interactions with other legal regimes (Privacy Act 1988 (Cth), PPIPA, HRIPA, Workplace Surveillance Act 2005 (NSW), Fair Work Act 2009 (Cth), legal professional privilege, commercial confidence, or intellectual property) but does not resolve them.

