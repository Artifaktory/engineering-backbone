# Project configuration and credential supply

Use this with the [core policy](../agent-governance/core.md),
[testing contract](../quality/testing.md) and [CI/CD contract](../quality/ci-cd.md).
These are original Backbone rules for an adopted project, informed by the source
notes below. They impose no secret-manager vendor, framework or universal loader.
Existing stronger access, review and operating controls remain binding.

## One declared configuration contract

The project owner records the applicable local, test, CI and production contexts,
component owner, actual loader, sources and precedence for each component. Native
manifest/configuration locations remain native. Shared nonsecret files belong in
`config/`; actual credentials remain outside version control and model context.

| Item | Ownership and purpose |
| --- | --- |
| Root `.env.example` | Project-owned, versioned names/comments and harmless placeholders only; no real secret values |
| `config/environment.json` | Project-owned register of names, types, components, purpose, secret classification and required contexts |
| Local `.env` or approved secret source | Real local values, untracked and access-controlled; only selected processes receive them |
| Actual component loader | Project-selected framework/native mechanism; document its location, loading and precedence |
| CI/production credential delivery | Reviewed job/service-scoped secret references or injection; no copied production `.env` on a general PR runner |

The Backbone source register is empty because its tooling requires no application
secrets. An empty register proves no application's credentials are configured.
Add relevant metadata when selecting a component; avoid a mandatory catalogue of
imaginary provider keys. If a framework requires `apps/<component>/.env.example`,
keep it there and document its relationship to the shared register.

## Register format and checker

The JSON object has exactly `version` (integer `1`) and `variables` (at most 256
entries). Each entry has exactly the following fields; a public enum additionally
has `choices`:

| Field | Meaning |
| --- | --- |
| `name` | Uppercase identifier: starts with `A`–`Z`, followed by at most 127 uppercase letters, digits or underscores |
| `component` | Nonempty component identifier/description, at most 1024 characters |
| `purpose` | Nonempty purpose, at most 1024 characters; describe use, never a credential value |
| `type` | `string`, `integer`, `boolean` or `enum` |
| `secret` | Boolean classification; secret enum choices are prohibited |
| `required_in` | Distinct selection from `local`, `test`, `ci`, `production`; an empty list means optional in these contexts |
| `choices` | Required only for a nonsecret enum: 1–64 distinct nonempty public strings, at most 1024 characters each |

No `value`, default, secret example or unknown field is accepted. Metadata does
not store or authenticate the actual secret. The project reviews its suitability.
The checker never checks whether a credential works against a service.

```sh
python .engineering-backbone/src/environment.py --environment local
python .engineering-backbone/src/environment.py --environment test
python .engineering-backbone/src/environment.py --environment local --env-file .env
```

`--root` selects the repository directory; `--contract` selects another register
relative to it. Both the contract and explicitly selected env file must be regular
UTF-8 files inside that root, without symbolic-link ancestors. Input files are
limited to 1 MiB and individual values to 65536 characters. These input constraints
are checker behavior, not a general access-control or secret-storage mechanism.

By default the checker examines only declared names in its inherited process
environment. It does not search for or load `.env`. With `--env-file`, the grammar
is deliberately limited to blank/comment lines and literal `KEY=VALUE` lines:

- Whole comment lines may start with optional whitespace followed by `#`.
- Keys have the declared uppercase spelling and no surrounding whitespace.
- Everything after the first `=` is literal, including spaces, quotes, `$`, `#`
  and backticks. There is no quote removal, escaping, interpolation, shell sourcing,
  command substitution, multiline value or `export` prefix.
- Duplicate/unknown keys, malformed lines and NUL characters fail. Process values
  override file values, including an explicitly empty process value.
- A required absent/empty value fails. Optional absent/empty values are allowed.
  Integers use optional `+`/`-` and digits only; booleans are exactly `true` or
  `false`; public enums must match a declared choice. Other strings stay literal.

The checker returns nonzero for invalid inputs and prints only declared variable
names or input line numbers with safe reasons. It never prints supplied values,
raw input lines, environment dumps or parser tracebacks. Its `PASS` covers only
the declared metadata and supplied values in the selected context. It does not
modify the calling shell, export variables to the application or implement the
application's native loader. Choose and test that loader separately; do not assume
Next.js, Python, Docker and other tools share the checker's file grammar or order.

## Agent and process access

Keep one authority for credentials and supply only the task-scoped capability the
authorized process needs. Planner and reviewer roles normally need no credential
values. A subprocess can use a secret without the model reading its raw value.
Do not put values in prompts, command arguments, tracked files, reports, screenshots
or logs. Read-only code access does not automatically authorize reading `.env`.

`.gitignore` prevents ordinary Git inclusion; it is not OS isolation, a host tool
deny rule or protection against an agent with shell/file access. Set actual host,
filesystem, broker or secret-store permissions for the selected client. An adapter
declaration or an ignored file alone does not prove enforcement. Verify safe
denial/redaction on the actual host before claiming a credential boundary.

Use separate credentials for relevant environments, least privilege and short
lifetimes where supported. General build/PR runners receive no production secrets.
Provide CI credentials only to the reviewed job/environment that needs them; avoid
global inherited secret bags. Keep server-only values out of browser bundles and
public client-prefixed variables. Public exposure is a property of the selected
framework/build, not the register's `secret` flag.

Record the credential owner, authorized consumers, delivery reference, rotation
and revocation procedure, expiry/monitoring and recovery path without values. On
suspected disclosure, revoke/rotate through the authorized provider process,
identify affected outputs and retain a redacted incident record. Deleting a value
from today's file does not revoke it or remove prior copies.

## Verification and source notes

Before an environment is considered usable, verify the selected loader, missing
and invalid input behavior, environment separation, redaction and authorized
process access. Use fake credentials for regression tests. Real service access,
native agent loading and CI execution require their own authorized evidence.

The [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
was inspected on 2026-10-21. It informs least-privilege access, lifecycle/rotation,
secure delivery and protection against disclosure. It also explains that process
environment values may leak through logs/dumps and discusses managed file/in-memory
delivery. A local `.env` is one project option, not a universally preferred secret
store. Our JSON fields, literal grammar, size limits and checker are Backbone
choices; this document asserts no external certification or clause conformity.
