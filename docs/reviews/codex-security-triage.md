# Codex identity-security Full triage

Full base: `8d4728d92a0125452b223f2fa99226fc8fc8cd0d`.
Full head: `c04cc8f966cbb48534e9fc98a4ca408460388c25`.
Patch SHA-256:
`087799c8f6eee49605e8f20f4b0be727f9d48ac3627466281c1d08c5b74ebdfa`.

Independent read-only sessions `codex_security_full_behavior` and
`codex_security_full_security` reviewed the same frozen snapshot. Both reported
one P1, high-confidence identity/path finding and no other confirmed in-scope
defect. Their disposable reproductions did not change the candidate.

| Finding | Decision before repair | Repair scope |
| --- | --- | --- |
| CB-1 | Confirmed, P1; duplicate cause shared with CS-1 | Reject noncanonical case-equivalent native path spellings |
| CS-1 | Confirmed, P1; root cause shared with CB-1 | Cover `.CODEX`, `Agents` and `CONFIG.TOML` lookup forms, including coexistence with canonical paths |

The new guard looked for exact directory-name membership `.codex` and exact child
paths `agents`/`config.toml`. Linux direct checks returned no errors for regular
nested case-variant fixtures claiming `backbone_reviewer`. The behavior reviewer
also ran the actual pinned historical-tooling shell: it exited 0 and reported
structural PASS for the `.CODEX` collision. Released Codex joins those literal
paths through filesystem metadata, so case-insensitive Windows/macOS lookup can
load the alternate spelling and later project layers can replace the role.
This is within the authorized identity/path repair and AC-1/AC-2/AC-3/AC-5.

Fix only this confirmed cause: fail closed on case-equivalent noncanonical native
containers/config filenames; retain case-sensitive role names and exact `.toml`
extensions. Add direct source/consumer and actual old-tooling workflow negatives,
including canonical/alternate coexistence. Refresh the current fingerprint and
compiled guard; never approve the unmerged initial implementation fingerprint as
a historical identity. Update the path-ambiguity wording and check record.

The source-based case-insensitive impact is not a live Codex or Windows test and
does not establish permission elevation. Generic application cwd aliases and
host/live overrides remain the explicitly documented separate runtime boundary.
No new roles, skills, permissions or downstream actions are authorized by triage.
Delta must use prior head above, repaired head, both IDs and direct regressions.

## External published Full: CP-1

Remote head `d61f96a6ff0816255a7371f0e0b4c7328ac51962` has the same tree as local
final `ed780777a59c6e84c556f72239f300a49d274a36`. The advisory provider reported
[CP-1, P2](https://github.com/Artifaktory/engineering-backbone/pull/7#discussion_r4249744760):
case-equivalent `.CODEX`/`.CoDeX` regular files and symlinks to files appear in
`os.walk` filenames, while the repaired casing check inspected only subdirectories.

Decision before repair: **confirmed, P2, high confidence**. The independent
`codex_security_full_security` session reproduced root/nested file and
symlink-to-file forms in disposable fixtures; all returned no guard error.
Canonical/alternate file-directory coexistence is ambiguous on case-insensitive
Windows checkout. This concerns portable checkout/role availability, not a newly
proved instruction substitution or permission escalation.

The authorized fix extends the same case-name check to `subdirs + filenames`,
recompiles the guard/current fingerprint and adds source/consumer plus actual
historical-workflow negatives. Preserve paths/bytes, native name/extension case
semantics and the existing runtime boundaries. CP-1 is a direct continuation of
the scoped path-ambiguity repair; no new Full scope or role/skill rollout is needed.
