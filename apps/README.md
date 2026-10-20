# Product applications

Keep independently built or deployed applications here. `frontend/`, `backend/`
and `automation/` are optional starting places, currently empty except for guidance.
Remove unused placeholders when adopting the structure in a project.

| Application | Code | Tests | Native dependency and build files |
| --- | --- | --- | --- |
| Web UI | `frontend/src/` | `frontend/tst/` | At `frontend/`, e.g. package.json, package lock, tsconfig.json |
| API or service | `backend/src/` | `backend/tst/` | At `backend/`, e.g. pyproject.toml and its chosen resolution file |
| Agent/automation application | `automation/src/` | `automation/tst/` | At `automation/`, e.g. package.json, package lock, tsconfig.json |

These are locations, not a selection of frameworks, package managers or versions.
A future Mastra application can use `automation/src/mastra/` for its agents, tools,
workflows and scorers. Desktop or other applications can add `apps/<name>/` with
`src/` and `tst/`. Keep files required by a framework at its native component root;
document any framework-required discovery path instead of breaking the build.
Repository-wide workspace/build files belong at the repository root when needed.
