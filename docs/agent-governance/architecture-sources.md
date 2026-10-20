# Architecture source provenance

The public official pages below were inspected on 2026-10-20. They inform the
[Backbone architecture contract](architecture.md); they are not a claim that its
wording or templates are prescribed verbatim by those publications. The ISO entries
identify published editions and public scopes. Full normative texts and clause
conformance were not assessed. Draft or future editions are not silently adopted.

| Source | Public scope used | Backbone application and limit |
| --- | --- | --- |
| [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) | Requirements engineering processes and the associated information items and formats. | Orientation for identified, attributable requirements and their relationship to design. Our specific dispositions, links and gate wording are organization-owned rules. |
| [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) | Architecture descriptions and related concepts, viewpoints and model kinds; distinguishes architecture from its description. It does not select authoring tools, notation, methods or document media. | Orientation for concerns, useful views and explicit relationships. The contract remains tool agnostic; document completeness is distinct from architectural fitness. |
| [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html) | Product quality model supporting specification, measurement and evaluation through the lifecycle. | Consider applicable qualities and express project goals as assessable scenarios. The model supplies neither universal target values nor evidence that a system meets them. |
| [ISO/IEC/IEEE 42020:2019](https://www.iso.org/standard/68982.html) | Architecture processes covering governance, management, architecting and support over an architecture's life. | Orientation for responsibility and continuing evolution. No wholesale process adoption or compliance claim for small projects. |
| [ISO/IEC/IEEE 42030:2019](https://www.iso.org/standard/73436.html) | Framework for architecture evaluation and its organization. | Orientation for scoped evaluation, stakeholder value, risks and recorded conclusions. A description review alone is not proof of the architecture's behavior. |

The methods below are distinct from ISO standards. We use their ideas to organize
original Backbone prompts and review questions; no third-party template text is
reproduced here. The common workflow is a proportional adaptation, not a claim to
have performed a complete named method.

| Method and official source | Application and boundary |
| --- | --- |
| [arc42 overview](https://arc42.org/overview/) and [method](https://arc42.org/method/) | The twelve content areas provide a useful completeness map. Recurring clarification, design, communication, implementation support and evaluation allow feedback. Projects combine or reference content according to risk and need; twelve files are not required. arc42 is by Peter Hruschka and Gernot Starke; its published template is CC BY-SA 4.0. The Backbone prompts are newly written and do not redistribute that template. |
| [arc42 quality scenarios](https://docs.arc42.org/section-10/) | Make qualities concrete through relevant conditions, stimuli and observable responses, including failure and change scenarios. Thresholds and priorities come from the project. |
| [C4 diagrams](https://c4model.com/diagrams) | Useful structural levels and supporting dynamic/deployment views; use only levels that answer relevant questions. C4, a specific renderer and Docker are not required. |
| [MADR](https://adr.github.io/madr/decisions/adr-template.html) | Context, drivers, credible options, rationale, consequences and confirmation inform significant decision records. There is no requirement to create an ADR for every local coding choice. |
| [SEI Attribute-Driven Design](https://www.sei.cmu.edu/library/attribute-driven-design-method-collection/) | Derive design work from functional needs, quality scenarios and constraints; refine responsibilities and interfaces iteratively. The contract does not claim to implement the full ADD method. |
| [SEI Quality Attribute Workshop](https://sei.cmu.edu/library/quality-attribute-workshop-collection/) | Clarify and prioritize important quality scenarios before an architecture is available. A full facilitated QAW is optional, not a default meeting requirement. |
| [SEI Architecture Tradeoff Analysis Method](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/) | Scenario-based evaluation, risks and tradeoffs inform independent review. The lightweight Backbone review must not be represented as a full ATAM evaluation. |

Sphinx-Needs and LikeC4 are possible project tools mentioned in the contract, not
sources of normative authority or integrations installed by this delivery. Projects
choose and verify their own mappings. A future regulated or clause-based profile
needs the full applicable material, qualified interpretation, explicit obligations,
project applicability and its required independent evidence through a separately
reviewed change. Neither an agent review nor structural validation certifies that.
