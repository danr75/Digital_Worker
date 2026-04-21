# Response to notice under s 118(1)(a1)
# Work Health and Safety Amendment (Digital Work Systems) Act 2026 (NSW)

**From:** {{ pcbu_name | default("[PCBU]") }}
**Represented by:** {{ pcbu_representative | default("[name, role]") }}
**To:** {{ eph_name | default("[Entry permit holder]") }}
**Workplace:** {{ workplace | default("[workplace address]") }}
**In reply to notice dated:** {{ notice_date | default("[date]") }}
**Date:** {{ response_date | default("[date]") }}

---

## 1. Scope of response

This response is to the notice issued under **s 118(1)(a1)** concerning the
{{ scenario_title }}.

The PCBU acknowledges the obligation to provide reasonable assistance and
sets out below:

1. What will be provided, and in what form (§ 2).
2. What is withheld, and on what ground (§ 3).
3. Timing and contact point for follow-up (§ 4).

## 2. Artefacts to be provided

{% for a in artefacts_provided -%}
### {{ loop.index }}. {{ a.artefact_name }}

- **Type:** {{ a.artefact_type }}
- **Access mode offered:** {{ a.access_mode_offered }}
- **Form:** {{ a.form_of_disclosure | default("To be confirmed with EPH") }}
- **Confidentiality undertaking proposed:** {{ "Yes" if a.requires_undertaking else "No" }}

{% endfor %}

## 3. Withheld or qualified

{% if artefacts_withheld -%}
The PCBU withholds or qualifies the following artefacts on the grounds set
out below:

{% for a in artefacts_withheld -%}
### {{ loop.index }}. {{ a.artefact_name }}

- **Ground for withholding:** {{ a.ground }}
- **Statutory basis / legal basis:** {{ a.basis }}
- **Proposed alternative:** {{ a.alternative | default("None — please discuss") }}

{% endfor %}
{% else -%}
The PCBU is not withholding any artefacts on this response. Any later
qualification will be communicated promptly with reasons.
{%- endif %}

## 4. Other-law matters noted

{% for f in other_law_flags -%}
- **{{ f.name }}** — {{ f.guidance }}
{% endfor %}

Where access is proposed subject to a confidentiality undertaking, a draft
is attached (or will be exchanged by email).

## 5. Timing and contact

{{ notice_period_guidance }}

Primary contact for this response:
- **Name:** {{ contact_name | default("[name]") }}
- **Role:** {{ contact_role | default("[role]") }}
- **Email / phone:** {{ contact_details | default("[details]") }}

---

{{ standard_disclaimer }}

{% if ai_assisted -%}
{{ ai_assisted_label }}
{%- endif %}
