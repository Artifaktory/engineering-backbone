# Independent checks after Full-1 repairs

Checker: `starter_quality`; Linux, hash-locked Python 3.12.14. This is a new
independent run on a separate clean frozen worktree, preserving the original
[521-test result](checks.md) and its snapshot unchanged.

- Actual base: `4e74c7e5f3a07430768f670c4271c1e1a0e28f68`.
- Repaired head: `bb794a6b05e35f168ee90d4dcbe5055f674eeead`.
- Tree: `b96337072a048afa37eee2135f3fafeaa76f8782`.
- Base-to-head binary patch SHA256: `fba134f81573d5100933bf63a2df6ac169c6ab8d34c90df1b86e9cd6b0abbfc9`.
- Prior Full head: `f0230d0da90b17ef52932ff027529acd23d73f51`.
- Full-to-repair binary patch SHA256:
  `1913af276440e84684ec4e7bae5787f8b46ac9687732576af684e0690894de46`.

The unchanged actual base-owned validator ran from its separate base checkout
with `--root CANDIDATE --trusted-base BASE`; candidate code did not replace it.
`PY` means the existing isolated interpreter. Full argv, cwd, timestamps, identities
and log hashes are in ignored `artifacts/starter-quality-final/`.

| Required gate | Exit | Seconds | Log SHA256 |
| --- | --- | --- | --- |
| candidate-validator | 0 | 1.309 | `07604dad0ce23e9a3291888da5b1f5fb1e48d63eee763a517af23015c68eb6af` |
| trusted-base-validator | 0 | 1.166 | `d28f15ddd16c8ae14e075b85bfff440c3903913fa5ad810e4e6d7e4bc1d229b1` |
| source-dependencies | 0 | 0.344 | `4c8826eb1d965d4f44ac880d328b943916f62ff61c70af306cdc80400da82ee5` |
| committed-whitespace | 0 | 0.007 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| repair-whitespace | 0 | 0.007 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| protected-paths | 0 | 0.003 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| python-version | 0 | 0.002 | `4c3569f5da09975434dd9fd9a91fadbc4367a91d8f3c3fab59e9241ab9ee4bd8` |
| compiler-toolchain_fingerprint | 0 | 1.759 | `5aeb70cd53318be3547180658775efe13a7162e841d38922f047e88035107c9c` |
| compiler-workflow_kit | 0 | 0.053 | `eb9708a2e83615ae1bec5707088a89f48ffbd2b83a3c0623dca3b8a138175cd4` |
| compiler-navigation | 0 | 0.089 | `f5acf715a03db96a191bdf0d036c4cfc8708079fafa3e08f149ee51564b2fbf2` |
| compiler-quality_framework | 0 | 0.104 | `649ebe6bdb8a344d0a7dec260dd3e57744a59dfc34f6d35c64ad36271a92d6b5` |

Commands are the candidate validator, actual base-owned validator, source dependency
check, all four maintenance compilers in `--check` mode, Python version, committed
base/head whitespace, committed Full-head/repair-head whitespace and the exact
protected-path comparison listed in the original check record. No protected path
changed. Compiler/fingerprint authority and previous delivery history remain intact.

## Complete suite

```sh
PY -m unittest discover -s .engineering-backbone/tst -t .engineering-backbone -v
```

**PASS: 528 tests, zero failures/errors/skips, exit 0;
684.798 seconds unittest / 685.554 seconds wrapper.**

Full-log SHA256: `5341628170577ac7a4cd78321c0da9c6add74fe0a524fa6ffdf00ac8c87a4240`.
The checker reconfirmed final identity, clean tracked state, actual base identity
and all indexed log hashes. The suite includes all fifteen environment and all
fifteen export tests, the eleven doctor/example tests and existing source/legacy
copy/update, trust-boundary, compiler and native-format regression cases.
Conditional Windows branches are not native Windows execution on this Linux host.

## Supplemental observations and limits

- Empty source register and explicit `.env.example`: exit 0, no invented credential.
- Actual development doctor: exit 0, prerequisites only.
- Actual source-linux doctor: exit 1, Docker CLI/daemon unavailable. This does not
  qualify a container or a runner.
- No native Windows, live provider loading, Docker image/daemon, runner fleet,
  access/isolation or successful remote CI evidence is claimed.

Both required scoped Delta reviews use this repaired frozen head and these actual
results. Their closure remains separate agent review advice. Later evidence-only
commits repeat candidate/base-owned validation and actual committed whitespace;
they do not change this executable review subject or turn queued CI into PASS.
