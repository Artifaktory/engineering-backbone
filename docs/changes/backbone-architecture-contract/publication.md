# BB-ARCH-015 publication record

## Observed publication

- Repository: `Artifaktory/engineering-backbone`.
- PR: [#21](https://github.com/Artifaktory/engineering-backbone/pull/21), created as
  a draft on 2026-10-20 at 15:56:51 UTC.
- Branch: `docs/architecture-contract`; target: `main`.
- Actual PR base and re-read remote `main`:
  `ae317bf30576914d4ed53856be4ae496c6ed64b3`.
- Published implementation and independent review subject:
  `f5860b5ec6ff31457c021c8a81cc0128f62fc468`.
- Its tree: `d4aa8b2a9024a3cb26293fede0bb4e6e13add713`.
- Its base-to-head binary patch SHA-256:
  `5440559beb213336e0c424cccf0b4e60ed7d48b30a789188168e27ef5996a287`.
- Earlier failed subject `1dbd1d68a7a23b8b38f532ed7a9dff8488642a57` is a reachable
  ancestor. Both subjects are GitHub-created commits fetched and frozen before
  their reported checks; unpublished local construction hashes are not review evidence.
- Observed initial hosted runs on the implementation: `Backbone quality`
  [39453057779](https://github.com/Artifaktory/engineering-backbone/actions/runs/39453057779)
  and `OpenCode native discovery`
  [39453057600](https://github.com/Artifaktory/engineering-backbone/actions/runs/39453057600)
  were queued at first inspection. This observation is not a PASS or final-head result.

## Final evidence child and closing observations

The next commit adds the completed reports, their acceptance mapping and this
record, and updates only this delivery's Task Packet/evidence metadata. Its parent
must remain the reviewed implementation above. Source, templates, tests, policies,
schemas, dependencies and workflows must remain byte-identical to that subject.
The copied independent reports retain their original bytes and scoped conclusions.

After that child is created, the publisher must inspect the exact evidence delta,
run the candidate and actual trusted-base structural checks, and run
`git diff --check ACTUAL_BASE FINAL_HEAD` plus
`git diff --check REVIEWED_HEAD FINAL_HEAD`. Record resolved full identities, tree,
binary patch digests, actual exit codes, report integrity and remote reachability
in the [PR description](https://github.com/Artifaktory/engineering-backbone/pull/21).
That external closing record avoids a self-referential claim that a commit embeds
its own final hash or the result of CI that had not run when it was written.

Observe hosted CI on the actual final head and link the run/job outcomes there.
Keep failures or unavailable/pending evidence explicit; do not relabel local tests
as final hosted results. A later change requires another final patch check and
updated publication identity. Substantive source changes also require the checks
and review treatment in the approved plan.

AC-7 is pending at this file's creation; its later disposition must be supported
by those actual closing observations. Human review/merge/release is separate.
No merge, release, deployment or downstream adoption was performed by this task.
