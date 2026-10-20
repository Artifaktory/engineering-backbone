# Legacy Copier compatibility

New projects use the actual reference repository layout described in the root
README. `templates/` remains only to preserve the already established Copier copy
and update contracts. Root `copier.yml` is its discovery entrypoint. Canonical code
and policy live at their new reference paths and are included here, not separately
maintained as another authority.

Legacy consumer output paths intentionally remain unchanged in this first refactor.
Do not remove this directory while running the Backbone compatibility suite or its
legacy fingerprint check. Retiring it or migrating an installed consumer requires
a separate reviewed change; no downstream application is performed by this PR.
