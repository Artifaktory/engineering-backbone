# Product configuration

Keep shared, non-secret application configuration and documented examples here.
Keep ecosystem discovery files (such as package manifests, tsconfig.json and
pyproject.toml) at the native root of the component that owns them. Environment
values, credentials and machine-specific settings are not committed.

The project-owned [environment register](environment.json) declares variable
names and metadata, never secret values. It is intentionally empty here because
Backbone tooling requires no application credentials. Add only variables selected
by the actual project; do not copy another application's provider/database keys.
The root `.env.example` is the harmless, versioned example. Actual `.env` and
`.env.*` values stay ignored; `.gitignore` does not prevent agent or process reads.

Follow the [configuration contract](../docs/operations/configuration.md) for the
closed register format, explicit literal-file checker, actual loader/precedence,
environment separation, credential access, rotation and redacted errors. Native
component `.env.example` locations remain possible where the selected framework
requires them; register the component and keep a single authority for each fact.
