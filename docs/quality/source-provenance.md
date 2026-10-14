# Quality source provenance

Reviewed on 2026-10-13. `standards/sources.json` is the machine-readable register;
`standards/rules.json` records the organization-owned derivation for each rule.
This record preserves what was actually inspected, rather than claiming access to
full normative material or a certification assessment.

| Official source | Inspected scope / reason for selection | Adoption boundary |
|---|---|---|
| [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html) | Published product-quality model scope, edition 2 | Orientation for measurable project goals; no full clauses adopted |
| [ISO/IEC/IEEE 12207:2026](https://www.iso.org/standard/90219.html) | Published software lifecycle scope, edition 2 | Orientation across development activities; no full clauses adopted |
| [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) | Published requirements-engineering scope, edition 2; revision draft separate | Orientation for requirements/traceability; no full clauses adopted |
| [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) | Published architecture-description scope, edition 2 | Orientation for design records; no full clauses adopted |
| [ISO/IEC/IEEE 29119-2:2021](https://www.iso.org/standard/79428.html) | Published test-process scope, edition 2 | Orientation for test strategy; no full clauses adopted |
| [ISO/IEC/IEEE 29119-3:2021](https://www.iso.org/standard/79429.html) | Published test-documentation scope, edition 2 | Orientation for records; no normative templates copied/adopted |
| [Microsoft public SDL practices](https://www.microsoft.com/en-us/securityengineering/sdl/practices) | Public security lifecycle guidance | Bounded security/design/test rules are our selections; Microsoft internal compliance is not claimed |
| [Google C++ guidance](https://google.github.io/styleguide/cppguide.html) | Public style/readability guidance and C++20 target | Reference-only; C++17 subset/toolchain integration pending |
| [Official Codex instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | Public discovery/override guidance | Context handoff guidance; actual intended-client loading unexecuted |
| [GitHub Copilot instruction support](https://docs.github.com/en/copilot/reference/custom-instructions-support) | Public instruction-type/client support matrix | Context handoff guidance; actual intended-client loading unexecuted |
| [IEC 61508-3:2010](https://webstore.iec.ch/en/publication/5517) | Public safety-related software scope, edition 2 | Disabled reference; full-text applicability and assessment pending |
| [IEC 62304:2006+AMD1:2015](https://webstore.iec.ch/en/publication/22794) | Public consolidated medical software lifecycle scope, edition 1.1 | Disabled reference; full-text applicability and assessment pending |

The published edition observations were checked on official ISO/IEC catalog pages.
The living Microsoft/Google/provider pages have no stable edition selected here;
their observation date is recorded explicitly. Rules are versioned organization
requirements, not a verbatim mirror or certification checklist. Candidate or
consumer changes cannot redefine these sources as enforcement authority.

A future clause-based profile needs authorized full-text access, exact section
mapping, applicability and interpretation review, qualified human ownership,
concrete obligations/checks and any required certification scheme. Treat that as a
separate scoped delivery. Updating a URL, catalog version or instruction file does
not prove normative compliance or installed client behavior.
