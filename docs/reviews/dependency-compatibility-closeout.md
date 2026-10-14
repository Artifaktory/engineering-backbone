# Dependency compatibility delivery evidence

Task: BB-DEPENDENCIES-009. This records scoped implementation and review evidence;
it is not human merge/release approval or universal platform compatibility.

## Reviewed snapshots

- Trusted main base: `229ac884c1a2ac70f0fb5c961bd517c9eaf740af`.
- Local Full head: `e6bc0faefe3de7c57e38aa618c4e9653fbe11ba5`;
  tree `89dcbdc011346155f17326b53642565ad4726c68`;
  patch SHA256 `6f55a2e666e097946585f9990143687e777069cbb3100bfa2217d3e6a8837cd0`.
- Local repaired head: `79fc21fbc5ff77938e3d2d952b90550cb36dedbd`;
  tree `3d0a14e4e629e27811c0c6daae2d04ef3ca324ec`;
  base-to-repaired patch SHA256 `47ac28de8cac66ca708d600b175ec0b0d76c6528ca03faa9523bc4316f4eb81f`.
- Repair Delta SHA256: `c695e338d61b3d3ce182269f3d1217418fd5b28d747e3012e6c094f5a4a840e5`.

GitHub API publication preserves exact trees while assigning new commit metadata:

| Stage | Public commit | Exact verified tree |
| --- | --- | --- |
| Full implementation | `c91a62cfdc549ca3e8c638c754a2ec890ebf94c8` | `89dcbdc011346155f17326b53642565ad4726c68` |
| Repaired implementation | `ccad5f6db400a135e7a55516c9c30e14a30a8cbe` | `3d0a14e4e629e27811c0c6daae2d04ef3ca324ec` |

The local and public commits above differ only in Git commit metadata/history,
not their corresponding file trees. This evidence-only closeout adds reports and
updates the Task Packet after the frozen repaired implementation; it does not
change executable code, Docker inputs, policy, catalogs, manifests or tests.

## Review and repair chain

The [independent plan review](dependency-compatibility-plan-review.md) preceded
implementation. The [behavior review](dependency-compatibility-full-behavior.md)
and [authority review](dependency-compatibility-full-authority.md) inspected the
same immutable Full snapshot. Both reported no confirmed in-scope findings in
their documented coverage; the broader suite remained pending at review time.

The original complete run subsequently executed 362 tests and failed three tests
with one cause: DEP-TEST-001, a stale explicit expected set of historical toolchain
identities. [Separate triage](dependency-compatibility-triage.md) confirmed it.
The two-line test-only repair adds the independently reproduced immediate
predecessor identity and preserves strict equality and all prior identities.
All three affected tests passed; [independent Delta review](dependency-compatibility-delta.md)
closed the finding with no confirmed direct repair regressions. The original
failure remains recorded rather than being relabeled successful.

The [independent execution record](dependency-compatibility-checks.md) records
all required local checks and the clean repaired full-suite rerun: **362/362 tests
passed**, zero failures/errors/skips, exact discovery-to-execution ID equality,
23 modules across four isolated processes, 368.83 seconds. All validators, four
compiler checks, source dependency consistency, Actionlint, whitespace, clean
locked installation and exact predecessor upgrade/attestation passed. Docker
build and offline container smoke remain pending actual GitHub CI execution.

The [bounded evidence review](dependency-compatibility-evidence-review.md)
verified the assembled reports and Task Packet on the preceding evidence snapshot.
Its verbatim report and this link are the only subsequent publication additions.

## Acceptance at publication

| Criterion | State and evidence |
| --- | --- |
| AC-1 shared policy | PASS: policy/dependencies.md, distribution/entrypoint changes and both Full reviews. Native files own concrete versions; application/tooling and library requirements differ. |
| AC-2 contract and routing | PASS: guard/schema, positive/negative tests, all-role/task context routing, effective approved check bindings and stale input rejection. |
| AC-3 upgrade compatibility | PASS: real Copier creation/update, exact trusted-main predecessor upgrade and workflow attestation, eight native/project files and 41 catalog JSON files byte-preserved. |
| AC-4 actual Docker inputs and execution | PENDING container execution: root Dockerfile, .dockerignore, compatibility document and agent links are tracked and source checks pass. Local engine unavailable; actual GitHub build/offline smoke required. |
| AC-5 deterministic checks | PASS: independent checks record and complete repaired 362-test rerun. Original failure and bounded repair evidence are retained. |
| AC-6 independent review chain | PASS: plan, two Full reviews, separate triage, bounded repair and Delta closure. |
| AC-7 publication/Codex | PENDING publication: verify remote tree and required files, request Codex visibly with fixed context, inspect CI and triage available remote findings. |

The source task remains ready for review, not completed, while remote obligations
are pending. Publication results belong to the PR conversation and a subsequent
bounded closeout update; do not infer success from planned CI commands.

## Limits and recovery

No local Docker engine was available. Registry header/body digest verification
and base-image metadata establish input identity only. Native Windows execution,
arbitrary PostgreSQL/application combinations and native agent instruction
loading were not attested. Each consumer retains its own supported matrix and
actual behavior tests. Existing catalogs, direct requirements and lock bytes are
unchanged; no consumer application Dockerfile or downstream repository was changed.

The optional contract installs inactive and requires reviewed seed/activation.
It does not silently disable inherited gates. If the proposed source change needs
recovery, leave the PR unmerged or revert it through a separately reviewed change;
do not remove active downstream contracts to bypass checks. Existing human merge,
release and stronger project controls remain binding.
