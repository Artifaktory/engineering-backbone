# BB-LAYOUT-013 prerequisite closeout

The existing main validator cannot interpret PR18's relocated source tree.
This prerequisite keeps the existing physical layout and prepares the trusted
validator to read either reviewed source layout. Candidate and base are resolved
independently. Consumer contracts, policy floors, schemas, permissions and gates
remain enforced. No candidate validator replaces the running trusted authority.

## Verified implementation

Base: `212608aa50ee517b3dd3107a9480da997222fd4f`.
Reviewed head: `aaa74e3dfc60836f8aae7c2751bc9dd889c52470`.
Tree: `fe6da7e734e7d6cdea508dc007649f03b903c423`.
Full binary patch SHA256:
`8f6ca8f0f22fe3065f392aed73c194be8aeebc7e0ee7b74680c871953e671969`.

[Independent checks](layout-compatibility-checks.md) record 441 tests passing,
four compiler checks, dependency and workflow-syntax checks, actual committed
base/head whitespace checks, and 505 unchanged inputs during execution. All 418
original methods and assertions remain; 413 protected existing blobs, including
59 original fixture blobs, are byte-identical to the base. The initial failed
run and its four triaged repairs remain recorded separately.

Actual old-main validation accepts this old-layout prerequisite. Its validator
accepts exact PR18 snapshots c501087 and corrected2ddfa803 against actual old
main, with independently verified Git blobs. Those are local transition checks,
not evidence that the prerequisite has already merged. Named new task/review
records and current links remain validated; candidate mappings grant no historical
exemption. Both independent Full reports record no confirmed in-scope findings.

| Acceptance | Evidence/disposition |
| --- | --- |
| AC-1 preserved layout and contracts | PASS: independent preservation audit and Full reviews. |
| AC-2 independent strict layout selection | PASS: four-layout matrix, negative tests and security probes. |
| AC-3 actual transition checks | PASS: actual old validator, actual old base and exact PR18 trees. |
| AC-4 rejection boundaries | PASS: 23 new cases plus existing negative suite and independent probes. |
| AC-5 complete checks and retained tests | PASS at reviewed head; post-evidence publication checks required again. |
| AC-6 independent review chain | PASS: plan, quality, two Full reviews and [separate triage](layout-compatibility-review-triage.md); no post-Full repair or Delta required. |
| AC-7 publication and human ordering | Pending at this commit; final identities and live CI results belong in the prerequisite PR description. |

## Publication and remaining human step

The final evidence-only commit is outside the frozen implementation snapshot.
Run both the new validator and actual old-main validator against that final tree,
then run the complete committed base-to-final-head whitespace check. Publish the
separate prerequisite PR against main and verify its remote trees and binary
patches against the local sequence. GitHub-created commit metadata can differ;
content correspondence must be exact. Record those post-commit checks and actual
remote CI conclusions in the PR description, avoiding a self-referential final
commit record. No local Docker/Podman execution is claimed.

A human must merge the reviewed prerequisite first. Only then can the actual
trusted main supply this validator to PR18. A later reviewed continuation must
integrate that actual main into PR18 without force push, reconcile moved runtime
and compiled files, and account for the newly added prerequisite test/evidence
paths. Recheck the new exact trusted transition, required tests and remote jobs.
PR18 remains blocked until that real base transition completes.

No merge, auto-merge, release, deployment, settings change, downstream application,
provider activation or permission expansion is included. Neither local structural
PASS nor independent AI review substitutes for human merge approval. Safe recovery
is a normal reviewed follow-up commit; historical records are retained.
