# Testing and CI/CD source provenance

Public primary sources were checked on **2026-10-21**. This register supports the
[testing contract](testing.md) and [CI/CD evidence contract](ci-cd.md). It extends
the explanation of existing quality, architecture and planning sources; it does
not replace the machine-readable catalog or change adopted profile authority.
The source repository keeps those earlier provenance records at
`docs/quality/source-provenance.md` and `docs/agent-governance/*-sources.md`.

ISO entries below describe verified published editions and public scopes. Their
complete normative texts were not assessed for clause conformity, and no external
template was copied. NASA/NIST guidance and ISTQB methods inform proportionate
original questions. SLSA requirements apply when a project makes a corresponding
claim. Exact `TST-*`/`CI-*` obligations, status words, document grouping and gate
mapping are Backbone-owned engineering choices, subject to stricter project rules.

## Reference register

| ID and official source | Verified contribution | Adoption limit |
| --- | --- | --- |
| **T-S01 — [ISO/IEC/IEEE 29119-1:2022](https://www.iso.org/standard/81291.html)** | Published edition 2; general concepts for the software-testing series. | Terminology orientation; this kit's words and schema crosswalk are not asserted to be prescribed ISO enums. |
| **T-S02 — [ISO/IEC/IEEE 29119-2:2021](https://www.iso.org/standard/79428.html)** | Published edition 2; generic processes for governing, managing and implementing testing across lifecycle models. | Main process anchor. No fixed hierarchy, development method, pipeline provider or universal mandatory test list is inferred. |
| **T-S03 — [ISO/IEC/IEEE 29119-3:2021](https://www.iso.org/standard/79429.html)** | Published edition 2; test documentation produced by Part 2 processes, across lifecycle models. | Informs record purposes. Backbone templates are original and may be combined or mapped to existing tools; no full normative template adoption is claimed. |
| **T-S04 — [ISO/IEC/IEEE 29119-4:2021](https://www.iso.org/standard/79430.html)** | Published edition 2; techniques supporting test design and implementation. | Informs deliberate technique selection. Every technique is not required for every project. |
| **T-S05 — [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html)** | Published edition 2; product-quality model supporting quality requirements, evaluation, testing goals and acceptance measures. | A model for identifying relevant qualities, not a ready-made test plan or universal numerical target. |
| **T-S06 — [ISO/IEC 20246:2017](https://www.iso.org/standard/67407.html)** | Published work-product review framework; confirmed current in 2022; reviews can apply across lifecycle phases and artifact types. | Supports review of requirements, design, code and other work products. A review does not replace required runtime evidence. |
| **T-S07 — [NASA Systems Engineering Handbook, 5.3 Product Verification](https://www.nasa.gov/reference/5-3-product-verification/)** | Public engineering guidance: project tailoring, verification methods/preparation, anomalies and revision-bound reports. | Adapt proportionately. NASA organizational approvals, flight qualification and mission-specific procedures are not imposed on unrelated projects. |
| **T-S08 — [NASA Systems Engineering Handbook, 5.4 Product Validation](https://www.nasa.gov/reference/5-4-product-validation/)** | Public guidance on intended use, stakeholder expectations, operating conditions and validation evidence. | Informs the distinction between specified behavior and usefulness in context; no NASA certification is claimed. |
| **T-S09 — [NIST SP 800-218, SSDF 1.1 Final](https://csrc.nist.gov/pubs/sp/800/218/final)** and [public text](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf) | February 2022 recommendations; PO.3 toolchains, PO.4 security-check criteria, PW.7 code review/analysis, PW.8 executable-code testing and PS.2 release integrity inform the selected duties. | Outcome- and risk-based secure-development recommendations; no prescribed tool or complete project testing method. [SSDF 1.2 initial public draft](https://csrc.nist.gov/pubs/sp/800/218/r1/ipd) is not adopted as final. |
| **T-S10 — [NIST SP 800-204D, Final](https://csrc.nist.gov/pubs/sp/800/204/d/final)** and [public text](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-204D.pdf) | February 2024 strategies for supply-chain security in DevSecOps CI/CD pipelines, in a cloud-native context. | Adapt relevant pipeline-security ideas; it is not a universal test specification or a mandate for cloud hosting. |
| **T-S11 — [SLSA v1.2](https://slsa.dev/spec/v1.2/)** | Approved industry specification: source/build tracks, increasing guarantees and provenance. | Optional assurance claims require the actual corresponding controls. A template, signature filename or runner label proves no level; own managed infrastructure is not automatically excluded by the term hosted build platform. |
| **T-S12 — [ISTQB CTFL v4.0 overview and syllabus v4.0.1](https://istqb.org/certifications/certified-tester-foundation-level-ctfl-v4-0/)** | Public professional-method framework: context, levels/types, static testing, design, risk, execution, configuration, defect management and completion. | Practical vocabulary and selection guidance; neither a mandatory project standard nor a requirement for staff certification, TDD, BDD or a particular tool. |

For agile applicability, [ISO/IEC TR 29119-6:2021](https://www.iso.org/standard/81293.html)
is optional guidance, a Technical Report rather than an additional mandatory
standard layer. Domain-specific safety, medical or other assurance regimes require
their own applicability, full-text and qualified-owner review; this generic kit
does not activate the existing disabled reference profiles.

## Rule-to-source crosswalk

| Testing group | Main sources | What remains our own contract |
| --- | --- | --- |
| TST-01 | T-S02, T-S03, T-S05, T-S07, T-S08 | Exact scope/ownership, source lineage, coverage dispositions and proportional combination. |
| TST-02 | T-S01, T-S04, T-S06, T-S07, T-S08, T-S12 | Local term boundaries and evidence claims across methods, levels, approaches and occasions. |
| TST-03 | T-S02, T-S05, T-S07, T-S09, T-S12 | Applicability matrix, risk-based minimum questions and preservation of adopted profile duties. |
| TST-04 | T-S02, T-S03, T-S07, T-S09 | Planning/readiness information, source links and unresolved-input gate handling. |
| TST-05 | T-S03, T-S04, T-S07, T-S12 | Concrete check-record questions and freedom to use executable tests as specification. |
| TST-06 | T-S03, T-S07, T-S09, T-S12 | Version/environment/data binding and explicit substitute/live limits. |
| TST-07 | T-S02, T-S03, T-S07, T-S09, T-S12 | Recorded attempts, triage, retry/quarantine boundaries and preservation of failed evidence. |
| TST-08 | T-S03, T-S07, T-S12 | Exact semantic dimensions and crosswalk to existing machine-supported states. |
| TST-09 | T-S02, T-S03, T-S06, T-S07, T-S08 | Scope-complete evidence assessment, independent review and inherited completion gates. |
| TST-10 | T-S02, T-S03, T-S07, T-S09, T-S12 | Changed-input applicability, context handoff and risk-based supported agent-chain coverage. |

The CI/CD contract identifies its own near-rule source notes, principally T-S02,
T-S03 and T-S09..11. Its mapping to the actual Backbone workflow kit preserves that
kit's current profile, phase and permission contract. Documentation alone does not
implement a new check kind, phase, scheduler, required-check setting or exception.

Local-runner selection and prohibition of GitHub artifact uploads are the user's
project/source operating constraints, not claims about a general ISO/NIST hosting
requirement. Other projects select their infrastructure within their applicable
authority. Evidence still needs an approved, accessible retention route. No source
reference grants credentials, installs a runner or authorizes publication/deployment.
