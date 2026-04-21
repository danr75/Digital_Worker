# Orientation brief for HSRs and workers
# Work Health and Safety Amendment (Digital Work Systems) Act 2026 (NSW)

**Prepared for:** {{ hsr_name | default("[HSR / worker]") }}
**Workplace:** {{ workplace | default("[workplace]") }}
**Date:** {{ issue_date | default("[date]") }}

---

## What this is

A plain-language brief explaining what the *Work Health and Safety Amendment
(Digital Work Systems) Act 2026* (NSW) lets you — and an entry permit holder
(EPH) acting for your union — ask about the **{{ scenario_title }}**.

## What the Act covers in this workplace

The system at your workplace is a **digital work system** under s 4 of the
Act. It uses the following kinds of technology:

{% for st in system_types -%}
- {{ st }}
{% endfor %}

## What risks the Act addresses (from s 21A(2))

{% for r in risk_types -%}
- {{ r }}
{% endfor %}

{% if warehouse_sub_patterns -%}
### Patterns identified in this workplace

{% for p in warehouse_sub_patterns -%}
- {{ p }}
{% endfor %}
{%- endif %}

## What can be looked at

An EPH can ask for "reasonable assistance" under s 118(1)(a1) to look at
parts of the digital work system. For the sub-component(s) in focus here,
the tool has identified the following kinds of artefact as relevant:

{% for a in artefacts -%}
- **{{ a.artefact_name }}** — {{ a.evidentiary_value }}
{% endfor %}

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

{{ standard_disclaimer }}

{% if ai_assisted -%}
{{ ai_assisted_label }}
{%- endif %}
