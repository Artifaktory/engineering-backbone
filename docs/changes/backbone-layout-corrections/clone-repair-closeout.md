# COP-CI-02 repair closeout

Both actual Foundation attempts at PR18 head
`2ddfa803688c70b556dc83bcf07a4c3911713be5` failed in the same existing historical
Copier upgrade subtest while Git copied a local loose object. The single unchanged
retry was exhausted. [Confirmed triage](clone-repair-triage.md) authorized a bounded
fixture transport repair; the exact Git/OS failure mechanism remains unproven.

The actual historical fixture now records a `git+file://` source, selecting Git's
transport for its real tagged copy/update operations. The same source, two tags,
negative installation-only cases, local-policy protection and trusted validation
remain. All 15 original assertions and both update call ASTs are unchanged; three
assertions additionally bind the real saved source and tag. No skip, retry,
exception suppression, hand-edited answers or dependency/workflow change exists.

Implementation head: `e2bd3c7dc881348967af28a6da99be992e94e122`.
Tree: `f94d11c832a8f5f0d492c1b8d7b6a71a91bec5c3`.
Repair baseline: `2ddfa803688c70b556dc83bcf07a4c3911713be5`.
Repair patch SHA256:
`9c5a498c61b72e2774e1fac84856e2f35423fbed5b5b4e79edcccded7efd6000`.

[Independent checks](clone-repair-checks.md) record 41 affected tests in 78.308
seconds passing, all 11 additional commands returning zero, 556 unchanged input
hashes, and 14 actual historical-fixture transport clones/upload-pack operations.
The [second Full](clone-repair-full-review.md) reports no confirmed in-scope
findings. Its [separate triage](clone-repair-review-triage.md) records final local
repair disposition. This completes the task's two-Full allowance; existing first
Full and all failed CI evidence remain preserved.

Local Git2.51.1/Python3.12.14 passing results do not establish the hosted
Git2.55.0/Python3.12.15 result. There are still 433 test methods; the new full
Foundation CI must run on the published changed head. No further unchanged retry
is approved by this record if that run fails; diagnose its actual failure.

After the final evidence commit, rerun structural validation and all committed
patch checks from original main212608, original correctionc501 and repair2ddfa803
to the exact final head. Verify every published tree/patch against the local
sequence. Record those post-commit identities, command exits and actual CI in
PR18's description. This avoids falsely checking only an empty worktree or
creating a self-referential publication-record commit loop.

The separately reviewed [prerequisite PR19](https://github.com/Artifaktory/engineering-backbone/pull/19)
prepares actual-main compatibility. A human must merge it before PR18 can obtain
that validator from trusted main, integrate moved files and rerun its final gate.
This test repair does not bypass the old trusted-base failure. No merge, release,
settings change, provider activation or downstream application was performed.
