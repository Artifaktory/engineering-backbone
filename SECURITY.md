# Security

Treat policy, validators, schemas, templates, native agent permissions and workflows
as a HIGH-risk control plane. See [the common policy](policy/core.md) and
[repository controls](docs/repository-controls.md).

Report sensitive vulnerabilities privately to the repository maintainers through
an established private channel. Use GitHub private reporting only if it is enabled;
do not post tokens, personal information or exploitable private infrastructure data
in public issues or review artifacts. No new external contact address is invented.

Never copy source-project secrets or deployment settings into the backbone. Consumer
updates preserve local stricter instructions and need independent review. Revoke
compromised credentials through the project's approved human-controlled process.

This bootstrap has no approved release yet. CI and schema-valid evidence do not
authenticate approvals or guarantee runtime isolation. Stop downstream distribution
when required protection/release controls remain unresolved.
