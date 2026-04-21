# Notice under s 118(1)(a1)
# Work Health and Safety Amendment (Digital Work Systems) Act 2026 (NSW)

**From:** {{ eph_name | default("[Entry permit holder]") }}
**Entry permit number:** {{ eph_permit_number | default("[permit number]") }}
**Union:** {{ eph_union | default("[union]") }}
**To:** {{ pcbu_name | default("[PCBU]") }}
**Workplace:** {{ workplace | default("[workplace address]") }}
**Date:** {{ issue_date | default("[date]") }}

---

## 1. Basis of notice

This notice is given under **section 118(1)(a1)** of the *Work Health and
Safety Act 2011* (NSW) as amended by the *Work Health and Safety Amendment
(Digital Work Systems) Act 2026* (NSW).

The entry permit holder suspects contraventions of:

{% for c in suspected_contraventions -%}
- **{{ c.section }}** — {{ c.description }}
{% endfor %}

## 2. Digital work system concerned

The digital work system concerned is the **{{ scenario_title }}**.

System type(s) identified (per the NSW AIAF alignment in these guidelines):

{% for st in system_types -%}
- {{ st }}
{% endfor %}

{% if warehouse_subcomponents -%}
Sub-component(s) in focus for this notice:

{% for sc in warehouse_subcomponents -%}
- {{ sc }}
{% endfor %}
{%- endif %}

## 3. Grounds

The grounds on which the entry permit holder suspects contravention include:

{% for g in grounds -%}
- {{ g }}
{% endfor %}

Risk types engaged under **s 21A(2)**:

{% for r in risk_types -%}
- {{ r }}
{% endfor %}

## 4. Assistance requested

In accordance with s 118(1)(a1), the PCBU is requested to provide reasonable
assistance to access and inspect the digital work system. Specifically:

{% for a in artefacts -%}
### {{ loop.index }}. {{ a.artefact_name }}

- **Type:** {{ a.artefact_type }}
- **Proposed access mode:** {{ a.proposed_access_method }}
- **Proportionality notes:** {{ a.proportionality_notes }}
- **Evidentiary value:** {{ a.evidentiary_value }}

{% endfor %}

**Overall access mode requested:** {{ access_mode }}

## 5. Timing

{{ notice_period_guidance }}

A response is sought by **{{ response_due_date | default("[date — allow the period recommended above]") }}**.

## 6. Other-law interactions acknowledged

The entry permit holder acknowledges the following other-law interactions,
which are raised for attention but not resolved by this notice:

{% for f in other_law_flags -%}
- **{{ f.name }}** — {{ f.guidance }}
{% endfor %}

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

{{ standard_disclaimer }}

{% if ai_assisted -%}
{{ ai_assisted_label }}
{%- endif %}
