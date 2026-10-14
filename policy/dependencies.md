# Dependency compatibility policy

Policy version **1.0.0** extends the core and quality authority without replacing
project instructions, scoped authorization or existing review and human gates.
The source uses `policy/dependencies.md`; consumers receive the same text as
`.engineering-backbone/dependency-policy.md`. An active project-owned
`.engineering-backbone/dependencies.json` adopts its component contract. Legacy
absence and inactive seeds make no dependency-conformance claim; existing project
requirements remain binding. The Backbone source applies this policy through its
tracked `docs/dependency-compatibility.md` and source checks.

## Version authority and supported combinations

Native manifests, reviewed resolution files and runtime/container configuration
are the authoritative version sources. Reference them from each component's
compatibility document; do not maintain duplicate package-version lists in prose.
Record the component kind, package manager/toolchain, supported runtime and target
platforms, important coupled dependencies, actual check IDs and coverage limits.
Projects choose these facts; this policy does not impose one global stack version.

- Applications and tooling require a concrete reviewed resolution of direct and
  transitive dependencies, with a reproducible installation command. Commit the
  lockfile or ecosystem-equivalent resolution artifact and keep it consistent with
  its manifest. Use integrity hashes where the selected tooling supports them.
- Published libraries declare justified supported dependency ranges in their
  package metadata. Document and test relevant boundary/coupled combinations and
  a reproducible test environment. A development lockfile does not establish
  compatibility for every supported downstream installation.
- Include runtime, package-manager, native build toolchain and container inputs in
  the reviewed combination. Pin external Docker base images by verified immutable
  digest, documenting the registry and target platform. Mutable tags or `latest`
  alone cannot identify a reproducible base. Refresh pins through tested update
  PRs; immutability is not permission to leave security updates unattended.
- Track real required inputs in Git, including Dockerfiles and compatibility
  documents. Installation instructions or placeholders alone do not satisfy this
  requirement. Do not commit secrets or generated environments.

## Change and agent decision contract

Choose or update dependencies only within the authorized task. Explain their need,
the intended version constraints, affected combinations and material transitive
changes. Update manifests, resolution artifacts and affected runtime/container
inputs together. Keep unrelated updates out of the change. Major versions and
changes to promised runtime/platform support require corresponding plan, migration
and review coverage; a patch/minor label alone does not establish compatibility.

Agents may select suitable packages and versions and make routine updates within
the reviewed project constraints without a separate approval solely for that
choice. Preserve existing stronger gates. Do not silently bypass peer/version
conflicts, ignore constraints, delete locks, use forced installs, or loosen bounds
to obtain a green check. Existing reviewed resolver settings remain project facts;
any necessary change needs explicit rationale and compatibility evidence in the
normal review. An exception cannot disable an inherited structural requirement;
that needs a separately reviewed contract migration.

## Required evidence

1. Perform a clean reproducible installation using the reviewed resolution and
   check manifest/resolution consistency and declared dependency requirements.
   Fail on unresolved conflicts. For example, `npm ci` rejects a manifest/lock
   mismatch; `pip check` checks installed declared requirements. Select equivalent
   checks for the actual ecosystem rather than imposing either tool universally.
2. Build or compile the affected deliverable and execute its relevant unit, API
   and integration tests on the supported targets. Cover risky coupled upgrades
   and representative boundary combinations; justify matrix selection rather than
   claiming every possible version combination ran.
3. Use actual PostgreSQL for promised server/extension/driver and migration
   behavior, including prior data where affected. Mocks or SQLite cannot establish
   that compatibility. Promised Windows behavior needs native Windows evidence;
   a Linux container establishes only its exercised Linux behavior.
4. For declared Dockerfiles, build the actual image and run the component's smoke
   or integration checks. Check startup and relevant runtime behavior against the
   pinned inputs; Dockerfile syntax or an image scan alone is insufficient.
5. Record commands, environments, revisions, results and gaps for independent
   review. Missing or failed required evidence blocks the affected gate. Security
   and license checks complement compatibility checks; a clean scan, successful
   resolution, lockfile or hash receipt is not proof of application behavior.

The active contract binds existing PR check kinds `dependency`, `build` and `test`,
plus `container` for Dockerfiles. Commands must actually establish the claimed
evidence for that component. Structural validation checks paths and approved
bindings, not command semantics, test execution or universal compatibility.

## Navigation and maintenance

For an active contract, resolve through the approved navigation/quality guard.
Every context includes this policy and the dependency contract; affected components
add their compatibility document, manifests, resolution, runtime and Dockerfile
inputs plus effective approved check definitions. Receivers verify the complete
hashed context and read it before scoped work. Changed inputs require fresh
context. Missing required files or invalid bindings block the task.

Adoption requires active quality, workflows and navigation, a complete reviewed
inactive dependency seed, then a separate enabled-only activation. Preserve
inherited active components, kinds, document/artifact references and check IDs.
Copier preserves project-owned configuration and documentation; manually integrate
updated native instructions. Use matching reviewed guard/workflow pins. See
`docs/agent-navigation.md` in the source or
`.engineering-backbone/navigation-guide.md` when installed for exact routing and
activation rules. Scheduled maintenance and dependency update PRs use the existing
review/triage/fix/Delta process; no automatic merge or downstream application.

## Public references

Reviewed 2026-10-14. These primary sources inform the selected policy; they do not
impose an entire external guide or select a project's tool versions.

- [npm ci](https://docs.npmjs.com/cli/commands/npm-ci/): installation from a lockfile
  and failure on manifest/lock mismatch; preserve compatible project resolver settings.
- [pip check](https://pip.pypa.io/en/stable/cli/pip_check/): installed declared
  dependency consistency, not behavioral compatibility.
- [PyPA dependency metadata and requirements](https://packaging.python.org/en/latest/discussions/install-requires-vs-requirements/):
  supported library ranges and repeatable application environments have different purposes.
- [Docker build best practices](https://docs.docker.com/build/building/best-practices/):
  immutable base digests, reviewed updates and actual image build/test evidence.
