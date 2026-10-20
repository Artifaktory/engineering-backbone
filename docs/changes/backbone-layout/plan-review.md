# Independent layout plan review

Reviewer session: `layout_plan_review`, independent read-only plan reviewer.
Date: 2026-10-20. Base and checkout HEAD:
`212608aa50ee517b3dd3107a9480da997222fd4f`.
No implementation changes existed during this review; only the four proposed
planning documents were inspected. This report is plan evidence, not an
implementation approval, authenticated human approval or a merge decision.

## Reviewed immutable planning snapshot

| File | SHA256 |
| --- | --- |
| `plan.md` | `8f49577958cca3be3d29526b26040229ba78d1b39eaaaccdc6243c8002760a0f` |
| `task-packet.json` | `cf97c46cce17ab9449a21139046302d919fa3414e1c907314faa395b3e7b0146` |
| `layout-map.json` | `c907065edf050a7d30a2307243f4117c22307d957c61b54b83122000cc493b0d` |
| `mapping.md` | `10c9b171f1b41f68f8eacb71922e46aa5e20809dc761b78636f860c0f09512cd` |

The digest tuple above identifies the proposed plan because the planning files
were not yet committed. Later implementation Full reviews must bind their own
committed base/head and binary patch digest.

## Coverage and observations

Read the trusted-base `AGENTS.md`, `CONTRIBUTING.md` and `policy/core.md`; inspected
the validator's source/consumer path contract, native instruction references,
legacy templates and the proposed scope, mapping, acceptance and verification.

- Compared the map with `git ls-tree -r -l` at the base: all **495** tracked blobs
  appear exactly once, with **495 unique destinations**. Every recorded base blob
  and size matches Git. No absolute or parent-traversal destination was present.
- All fixture entries are marked byte-preserved. The map marks **152** entries
  byte-preserved in total, including **88** historical plan/review records.
- Validated the proposed Task Packet using the existing Draft 2020-12 schema:
  **zero schema errors**. Acceptance remains pending; this check proves format,
  not implementation or completion.
- The plan keeps one canonical policy, native discovery locations, explicit
  legacy consumer compatibility, dependency pins and negative checks. Empty
  product directories do not claim completed product functionality.
- The direct-copy contract names the project facts, source-only CI restrictions,
  inactive integrations and historical evidence that require project adoption.
  It does not claim a copied repository is automatically production-ready.
- The previous trusted validator remains exercised without candidate fallback,
  projection or catch-and-pass. The documented old-path incompatibility is a
  visible draft-PR merge blocker, not a passed migration gate.
- Independent quality checks, frozen behavior/security Full reviews, separate
  triage and bounded Delta repair review are required before publication claims.
  Container and native runtime gaps remain explicit.

## Finding and disposition

**LPLAN-01 — P2, trust-boundary clarification, high confidence.** The initial
historical-link design described a bounded crosswalk without naming its authority.
If an implementer read archive classifications or expected hashes from the
candidate's map, a candidate could label a current document as historical or
rewrite the expected bytes to avoid the intended checks. This would violate
AC-1/AC-3 and the requirement to keep current documents under normal validation.

The coordinator confirmed the finding before the planner amended the plan. The
reviewed final plan explicitly requires the executing trusted bundle or a reviewed
compiled literal as archive identity/hash/mapping authority, rejects candidate-map
authority, and requires negative relabel/hash-tampering tests. The clarification
is verified in the final planning snapshot above. **Disposition: resolved at plan
level; implementation and regression evidence remain required.**

## Result and limits

**NO UNRESOLVED CONFIRMED IN-SCOPE PLAN FINDINGS.** The bounded plan is suitable
to proceed to implementation and the documented review chain. No source code was
changed or certified by this reviewer. The 495-file relocation, actual direct-copy
behavior, compatibility suite, compiler fingerprints, container execution and
remote CI have not been established by this plan review. The intentional legacy
trusted-base incompatibility still blocks merge readiness.
