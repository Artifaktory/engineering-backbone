# Runtime and deployment infrastructure

Use `docker/<component>/Dockerfile` for component images with a documented build
context. Place selected orchestration, deployment and monitoring configuration in
clearly named subdirectories here. Root discovery files can remain at the root when
the chosen tool requires it; document their ownership.

`docker/engineering-backbone/Dockerfile` builds only Backbone's existing Python
validation tooling using the repository root as its context. It does not run a
frontend, API, database or automation application. Product containers and environments
are added in their own project, with actual build/smoke evidence.
