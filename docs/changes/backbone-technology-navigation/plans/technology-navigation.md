# Technology profiles and agent document navigation

## Task and authority

Task `BB-TECH-NAV-008` is authorized by the user's 2026-10-14 request to plan,
implement, check, independently review, publish a PR and request Codex review.
Base: `edde45d7ce79f6c2c3d70bd0b8ece0a8d9eecb12` on `main`. This is HIGH-risk
control-plane work. No merge, release, deployment, downstream adoption or runner
migration is authorized here. Existing core, role and human gates remain binding.

## Design

1. Preserve the existing compiler-owned quality catalog byte-for-byte. Its trusted
   predecessor rejects replacement even for additive entries; do not weaken that
   gate. Add a bounded versioned extension at `standards/technologies/`, governed
   by the same core and quality policy. Its selected obligations only add duties.
2. Cover Python, JavaScript, TypeScript, Java, C#, Go, C, C++, PHP, HTML, CSS, SQL,
   PostgreSQL, PowerShell, Bash, JSON, YAML, Dockerfile, GitHub Actions, Windows,
   Linux, Node, .NET, JVM, Docker, React, Next.js and FastAPI. Record checked public
   sources and selected obligations, not blanket certification or compatibility.
   Mandatory rules bind existing workflow check kinds; guidance distinguishes
   SHOULD defaults from free implementation choices. No unreviewed toolchain,
   universal design pattern or runtime upgrade is imposed on consumers.
3. Add project-owned `.engineering-backbone/navigation.json`: inactive seed,
   explicit document IDs, role/task routes and components with literal path prefixes,
   selected technology profiles and additional authoritative documents. A request
   references an existing Task Packet and supplies task type, paths/components and
   snapshot identity. Derive role and authorized scope from the packet. Union all
   matching components; reject unknown, unmatched or contradictory context.
4. A self-contained deterministic resolver adds mandatory core/project/quality
   documents, relevant native instructions, selected catalog obligations and actual
   check bindings. Validate regular repository-local paths, exact case, anchors,
   bounded JSON, duplicates and symlinks. Declared exceptional local instructions
   remain subject to independent review; no automatic precedence bypass.
5. Emit a versioned context with exact document hashes, catalog/profile/rule/check
   identities, Task Packet hash and request digest. Verify handoffs by recomputing
   the complete context; missing/altered/stale fields fail. A digest is integrity
   evidence, not authentication, semantic approval or proof of provider loading.
6. Compile the resolver and extension as reviewed literals into the existing trusted
   quality guard; never import candidate code for validation. Preserve standalone
   AST-extracted guard tests and embed the same implementation into the workflow.
   Expose resolve/verify commands through the distributed quality tooling.
7. Copier installs optional inactive navigation and managed extension assets when
   the quality package is selected. Existing native instructions and project-owned
   navigation are preserved. Add short routing instructions to root/provider/role/
   skill templates and a shared guide; synchronize source and consumer paths.
   Active adoption requires a reviewed complete inactive seed and a separate
   enabled-only activation. Existing installations without navigation still work.
   Inherited active routes cannot silently disappear or weaken in a candidate.

## Verification and review

- Baseline source validation and compiler check before edits.
- Catalog positives and invalid-source/profile/check cases; real rendered consumer
  coverage for every selected profile without pretending to execute each language.
- Resolver scenarios: Python/PostgreSQL bugfix and migration, PowerShell Windows
  maintenance, Bash Linux/container work, architecture and independent review.
- Negative cases: missing/empty/renamed documents and anchors, case ambiguity,
  traversal/symlink, unknown technology or unmatched path, task-scope mismatch,
  stale/tampered/truncated handoff, removed active routing and invalid activation.
- Real Copier create/update, provider combinations, source/consumer path agreement,
  stronger local rules preserved, and predecessor validator compatibility.
- Existing compiler checks, full unittest suite, Actionlint where available and
  `git diff --check`; retain commands, exits and truthful limits in review records.
- Actual native Codex/Copilot discovery requires the supported signed-in client.
  Deterministic resolution or a model's receipt is not such a test. Record any
  explicit-context agent smoke separately and mark inaccessible client tests pending.
- Freeze one base/head/patch for two independent Full reviewers (behavior and
  authority/security), triage findings before fixes, then targeted tests and Delta
  review of confirmed fixes. Maximum two Full rounds unless justified by policy.
- Publish the reviewed PR, verify remote tree identity and CI, then request Codex
  review visibly on that PR. Keep absent or delayed external results explicit.

## Ownership

Catalog worker owns extension data, technology guidance, matching templates and
catalog tests. Navigation worker owns resolver, navigation schemas and focused
tests. Integrator owns trusted compilation, existing tooling/CI integration,
entrypoint/role wiring, adoption docs, review records and publication.
Independent reviewers do not edit the implementation under review.
