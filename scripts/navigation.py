#!/usr/bin/env python3
"""Reviewed navigation engine, compiled into the trusted quality guard.

No project code or commands run here. Context hashes record declared input
integrity, never authorization, client discovery or semantic conformance.
"""


def navigation_context(root, trusted_base=None, *, source=False, request=None,
                       expected=None, authority=None):
    """Validate routes and optionally resolve/verify a complete handoff context."""
    import fnmatch
    from functools import lru_cache
    import hashlib
    import json
    import os
    from pathlib import Path
    import re
    import stat

    technology_catalog_json = '{"version":"1.0.0","sources":[{"id":"TECH-SRC-PYTHON","title":"Python PEP 8","edition":"Living documentation observed 2026-10-14","url":"https://peps.python.org/pep-0008/","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Project consistency and compatibility; imports, public interfaces and documentation guidance."]},{"id":"TECH-SRC-DOCSTRINGS","title":"Python PEP 257","edition":"Living documentation observed 2026-10-14","url":"https://peps.python.org/pep-0257/","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Public docstring conventions; selected guidance, not a prescribed test or typing framework."]},{"id":"TECH-SRC-ECMASCRIPT","title":"TC39 ECMAScript control abstraction objects","edition":"Living draft titled ECMAScript 2027, observed 2026-10-14","url":"https://tc39.es/ecma262/multipage/control-abstraction-objects.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Promise fulfilled, rejected and pending states; the living draft is not a project language-version selection."]},{"id":"TECH-SRC-TYPESCRIPT","title":"TypeScript strict compiler option","edition":"Living documentation observed 2026-10-14","url":"https://www.typescriptlang.org/tsconfig/strict.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Strict option enables a family of type checks; future compiler versions can add checks."]},{"id":"TECH-SRC-JAVA","title":"Google Java Style Guide","edition":"Living documentation observed 2026-10-14","url":"https://google.github.io/styleguide/javaguide.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Formatting, naming and programming-practice guide scope; project selects compatible conventions."]},{"id":"TECH-SRC-CSHARP","title":"Microsoft C# coding conventions","edition":"Living documentation observed 2026-10-14","url":"https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Coding conventions and consistency guidance; compiler and language versions remain project decisions."]},{"id":"TECH-SRC-GO","title":"Effective Go","edition":"Living documentation observed 2026-10-14","url":"https://go.dev/doc/effective_go","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Formatting, names, errors and concurrency guidance; the page warns it is not a comprehensive modern Go guide."]},{"id":"TECH-SRC-C","title":"SEI CERT C Coding Standard publisher description","edition":"2016 edition; publisher scope observed 2026-10-14","url":"https://www.sei.cmu.edu/library/sei-cert-c-coding-standard-rules-for-developing-safe-reliable-and-secure-systems-2016-edition/","status":"observed","access":"public-scope-only","adoption":"reference-only","verified_sections":["Publisher confirms secure C coding scope and the 2016 edition. Full rule text was not retrieved; its download redirected to a registration form."]},{"id":"TECH-SRC-CPP","title":"C++ Core Guidelines","edition":"Living documentation observed 2026-10-14","url":"https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Resource, ownership and interface guidance scope; selected project obligations do not adopt the entire guide."]},{"id":"TECH-SRC-GOOGLE-CPP","title":"Google C++ Style Guide","edition":"Living documentation observed 2026-10-14","url":"https://google.github.io/styleguide/cppguide.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["C++ version section targets C++20; self-contained headers and direct includes; no universal exception policy is imported."]},{"id":"TECH-SRC-GOOGLETEST","title":"GoogleTest Primer","edition":"Living documentation observed 2026-10-14","url":"https://google.github.io/googletest/primer.html","status":"observed","access":"public-selected-sections","adoption":"tool-example-only","verified_sections":["Assertions, tests and fixtures as an optional test-framework example."]},{"id":"TECH-SRC-PHP","title":"PHP-FIG PER Coding Style","edition":"PER Coding Style 3.1, observed 2026-10-14","url":"https://www.php-fig.org/per/coding-style/","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["PER Coding Style 3.1 page and formatting guidance; selected PHP compatibility must be checked before adoption."]},{"id":"TECH-SRC-HTML","title":"WHATWG HTML semantics and structure","edition":"Living documentation observed 2026-10-14","url":"https://html.spec.whatwg.org/multipage/dom.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Element semantics, content models and accessibility-related definitions."]},{"id":"TECH-SRC-WCAG","title":"W3C Web Content Accessibility Guidelines 2.2","edition":"WCAG 2.2, observed 2026-10-14","url":"https://www.w3.org/TR/WCAG22/","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Accessibility success criteria and conformance structure; automated tests alone do not establish conformance."]},{"id":"TECH-SRC-CSS","title":"W3C CSS Snapshot 2026","edition":"W3C Group Note, 2026-06-22","url":"https://www.w3.org/TR/2026/NOTE-css-2026-20260622/","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Specification-module snapshot; explicitly not a browser-adoption compatibility profile."]},{"id":"TECH-SRC-SQL","title":"PostgreSQL SQL syntax","edition":"PostgreSQL 18 documentation","url":"https://www.postgresql.org/docs/18/sql-syntax.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["SQL language syntax overview for PostgreSQL; not a portable SQL dialect promise."]},{"id":"TECH-SRC-PG-CONSTRAINTS","title":"PostgreSQL constraints","edition":"PostgreSQL 18 documentation","url":"https://www.postgresql.org/docs/18/ddl-constraints.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Constraint behavior including check, not-null, unique, primary-key and foreign-key constraints."]},{"id":"TECH-SRC-PG-QUERIES","title":"PostgreSQL command execution functions","edition":"PostgreSQL 18 documentation","url":"https://www.postgresql.org/docs/18/libpq-exec.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Parameterized command execution through libpq; each application driver needs its own reviewed equivalent."]},{"id":"TECH-SRC-PG-TRANSACTIONS","title":"PostgreSQL transaction isolation","edition":"PostgreSQL 18 documentation","url":"https://www.postgresql.org/docs/18/transaction-iso.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Transaction isolation and concurrency behavior; no blanket retry or locking policy is prescribed."]},{"id":"TECH-SRC-PG-RESTORE","title":"PostgreSQL backup and restore","edition":"PostgreSQL 18 documentation","url":"https://www.postgresql.org/docs/18/backup.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Backup methods and restore guidance overview; project recovery goals and rehearsals are organization requirements."]},{"id":"TECH-SRC-POWERSHELL","title":"PowerShell try, catch and finally","edition":"PowerShell 7.5 documentation","url":"https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally?view=powershell-7.5","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Terminating error handling and resource cleanup; native process errors require separate treatment."]},{"id":"TECH-SRC-PSSCRIPTANALYZER","title":"PSScriptAnalyzer overview","edition":"Living documentation observed 2026-10-14","url":"https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/overview?view=ps-modules","status":"observed","access":"public-selected-sections","adoption":"tool-example-only","verified_sections":["Static script quality checks and configurable rules."]},{"id":"TECH-SRC-PESTER","title":"Pester quick start","edition":"Living documentation observed 2026-10-14","url":"https://pester.dev/docs/quick-start","status":"observed","access":"public-selected-sections","adoption":"tool-example-only","verified_sections":["Executable behavior tests and assertions as a PowerShell testing option."]},{"id":"TECH-SRC-SHELLCHECK","title":"ShellCheck SC2086","edition":"Living documentation observed 2026-10-14","url":"https://www.shellcheck.net/wiki/SC2086","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Quoting to control word splitting and glob expansion; intentional splitting needs an explicit reviewed design."]},{"id":"TECH-SRC-BASH","title":"GNU Bash Reference Manual","edition":"Indexed official manual observed 2026-10-14","url":"https://www.gnu.org/software/bash/manual/bash.html","status":"retrieval-limited","access":"indexed-summary-only","adoption":"reference-only","verified_sections":["Official indexed summary identifies quoting and exit status; direct page retrieval timed out, so no section-level adoption is claimed."]},{"id":"TECH-SRC-JSON","title":"RFC 8259 JSON","edition":"RFC 8259, December 2017","url":"https://www.rfc-editor.org/rfc/rfc8259","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["JSON syntax, duplicate member interoperability concerns and encoding."]},{"id":"TECH-SRC-YAML","title":"YAML specification 1.2.2","edition":"YAML 1.2.2","url":"https://yaml.org/spec/1.2.2/","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Mapping key uniqueness, representation model and schema-dependent scalar resolution."]},{"id":"TECH-SRC-ACTIONS","title":"GitHub Actions workflow syntax","edition":"Living documentation observed 2026-10-14","url":"https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Workflow events, permissions, job conditions and shell execution syntax."]},{"id":"TECH-SRC-DOCKER","title":"Docker build best practices","edition":"Living documentation observed 2026-10-14","url":"https://docs.docker.com/build/building/best-practices/","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Base image selection, digest pinning and limiting unnecessary image content."]},{"id":"TECH-SRC-DOCKER-SECRETS","title":"Docker build secrets","edition":"Living documentation observed 2026-10-14","url":"https://docs.docker.com/build/building/secrets/","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Build secret mounts and the risks of persisting secrets through build arguments or environment variables."]},{"id":"TECH-SRC-WINDOWS","title":"Microsoft Windows file and path naming","edition":"Living documentation observed 2026-10-14","url":"https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Reserved device names, path separators, case behavior and relative path interpretation."]},{"id":"TECH-SRC-LINUX","title":"Linux kernel user-space API guide","edition":"Living documentation observed 2026-10-14","url":"https://docs.kernel.org/userspace-api/index.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["User-space API documentation scope; distro, shell and native-test support remain project obligations."]},{"id":"TECH-SRC-NODE","title":"Node.js errors","edition":"Living documentation observed 2026-10-14","url":"https://nodejs.org/api/errors.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Error propagation and errors from asynchronous APIs; displayed runtime version is not adopted for consumers."]},{"id":"TECH-SRC-DOTNET","title":"Microsoft testing in .NET","edition":"Living documentation observed 2026-10-14","url":"https://learn.microsoft.com/en-us/dotnet/core/testing/","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Testing framework and test runner overview; target frameworks and runtime support are project choices."]},{"id":"TECH-SRC-JVM","title":"Java Virtual Machine Specification","edition":"Java SE 21 edition","url":"https://docs.oracle.com/javase/specs/jvms/se21/html/index.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Class-file format, loading, linking and execution model contents; selected JDK/runtime compatibility requires executable tests."]},{"id":"TECH-SRC-REACT","title":"Rules of React","edition":"Living documentation observed 2026-10-14","url":"https://react.dev/reference/rules","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Component and Hook purity, call order and use through React."]},{"id":"TECH-SRC-NEXTJS","title":"Next.js server and client components","edition":"Living documentation observed 2026-10-14","url":"https://nextjs.org/docs/app/getting-started/server-and-client-components","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Server/client boundaries, serializable props and avoiding environment poisoning."]},{"id":"TECH-SRC-FASTAPI","title":"FastAPI testing tutorial","edition":"Living documentation observed 2026-10-14","url":"https://fastapi.tiangolo.com/tutorial/testing/","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["TestClient-based requests and assertions; authorization, persistence and lifecycle coverage are project risk-based additions."]}],"rules":[{"id":"TECH-PYTHON-001","version":"1","statement":"MUST: Record supported Python versions and one compatible style/type configuration. Keep changed public interfaces documented; type-check new application boundaries, validate external input and preserve useful exception context. Bind lint, typecheck and behavior tests, including relevant failure paths. Document generated/vendor exclusions and legacy typing debt without silently widening them.","source_ids":["TECH-SRC-PYTHON","TECH-SRC-DOCSTRINGS"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"],["typecheck"],["test"]]},{"id":"TECH-JAVASCRIPT-001","version":"1","statement":"MUST: Record the ECMAScript target, supported hosts and module system. Validate external values, handle asynchronous rejection and avoid runtime code evaluation of untrusted input. Bind a consistent lint configuration and tests for observable success and failure behavior on the supported hosts.","source_ids":["TECH-SRC-ECMASCRIPT"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"],["test"]]},{"id":"TECH-TYPESCRIPT-001","version":"1","statement":"MUST: Record compiler, runtime and ECMAScript targets. Enable strict type checking for new components; inventory inherited exceptions and justify any new suppression or unsafe any at a boundary. Validate external data at runtime and handle asynchronous failures. Bind lint, typecheck and tests without disabling checks to pass.","source_ids":["TECH-SRC-TYPESCRIPT","TECH-SRC-ECMASCRIPT"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"],["typecheck"],["test"]]},{"id":"TECH-JAVA-001","version":"1","statement":"MUST: Record the supported JDK/language target and selected compatible style subset. Use a consistent formatter, preserve public contracts, close owned resources and handle exceptions without losing their cause. Bind compilation, lint/static analysis and tests on the promised runtime versions.","source_ids":["TECH-SRC-JAVA"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["build"],["lint"],["test"]]},{"id":"TECH-CSHARP-001","version":"1","statement":"MUST: Record C# language and target-framework versions. Configure consistent formatting and analyzers; make null handling, disposable-resource ownership and asynchronous cancellation explicit at affected boundaries. Bind compilation, lint/analyzer and behavior tests; justify suppressions in review.","source_ids":["TECH-SRC-CSHARP"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["build"],["lint"],["test"]]},{"id":"TECH-GO-001","version":"1","statement":"MUST: Record supported Go versions. Apply gofmt, handle returned errors and bound the lifetime of started goroutines and owned resources. Bind build, lint/static analysis and tests; assess race testing for changed shared-state code and record its result or concrete unsupported-platform limit.","source_ids":["TECH-SRC-GO"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["build"],["lint"],["test"]]},{"id":"TECH-C-001","version":"1","statement":"MUST: Record the C language edition, compiler targets and selected warning/analyzer configuration. Review buffer bounds, integer conversions, resource ownership and error returns in changed code. Bind build, lint/static analysis and boundary/failure tests; document sanitizer applicability and results for memory-risk changes.","source_ids":["TECH-SRC-C"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["build"],["lint"],["test"]]},{"id":"TECH-CPP-001","version":"1","statement":"MUST: Record the C++ edition, compiler targets and a compatible chosen guide subset. Make ownership explicit, use automatic resource lifetime management, keep public headers self-contained and adopt one reviewed exception/error policy. Resolve Google/Core Guidelines conflicts before work. Bind build, lint/static analysis and behavior tests, with appropriate lifetime and boundary checks.","source_ids":["TECH-SRC-CPP","TECH-SRC-GOOGLE-CPP","TECH-SRC-GOOGLETEST"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["build"],["lint"],["test"]]},{"id":"TECH-PHP-001","version":"1","statement":"MUST: Record supported PHP versions and a compatible PER/PSR style selection. Validate request and persistence boundaries, handle errors explicitly and document public interfaces. Bind syntax/style/static analysis and tests; preserve framework conventions where reviewed and compatible.","source_ids":["TECH-SRC-PHP"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"],["test"]]},{"id":"TECH-HTML-001","version":"1","statement":"MUST: Record supported browsers and the accessibility target. Use appropriate semantic elements, accessible names, labels and keyboard-operable controls. Bind markup lint/validation and rendered behavior tests; manually verify relevant accessibility criteria that automation cannot establish.","source_ids":["TECH-SRC-HTML","TECH-SRC-WCAG"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"],["browser","test"]]},{"id":"TECH-CSS-001","version":"1","statement":"MUST: Record supported browsers and responsive/accessibility requirements. Select compatible CSS features and a consistent lint configuration. Preserve focus visibility and content usability under required resizing/zoom. Bind lint and rendered layout/interaction tests for affected critical views.","source_ids":["TECH-SRC-CSS","TECH-SRC-WCAG"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"],["browser","test"]]},{"id":"TECH-SQL-001","version":"1","statement":"MUST: Record the database dialect and server/driver versions. Parameterize values; validate or safely select dynamic identifiers through the driver contract. State transaction boundaries and handle null semantics explicitly. Bind dialect-aware lint/validation and query behavior tests against the actual database dialect; a substitute dialect does not prove compatibility.","source_ids":["TECH-SRC-SQL","TECH-SRC-PG-QUERIES"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"],["test"]]},{"id":"TECH-POSTGRESQL-001","version":"1","statement":"MUST: Record supported PostgreSQL versions, extensions and driver settings. Use parameterized queries, appropriate constraints and least-privilege roles. Specify transaction/isolation and retry behavior. Bind real PostgreSQL integration tests and migration checks that preserve existing data; review lock/concurrency failure paths and rehearse restore or forward recovery according to the documented data-risk plan.","source_ids":["TECH-SRC-PG-CONSTRAINTS","TECH-SRC-PG-QUERIES","TECH-SRC-PG-TRANSACTIONS","TECH-SRC-PG-RESTORE"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["test"],["migration"]]},{"id":"TECH-POWERSHELL-001","version":"1","statement":"MUST: Record PowerShell edition/version and supported operating systems. Validate parameters, use literal-safe paths where appropriate, distinguish terminating/nonterminating errors from native process exit codes and clean up owned resources. Bind script analysis and behavior tests with failed commands, missing files and paths containing spaces; never log secrets.","source_ids":["TECH-SRC-POWERSHELL","TECH-SRC-PSSCRIPTANALYZER","TECH-SRC-PESTER"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"],["test"]]},{"id":"TECH-BASH-001","version":"1","statement":"MUST: Record the Bash interpreter version and target platforms; do not label Bash-specific code as portable sh. Quote expansions according to intended splitting/globbing, use argument arrays where appropriate, check command/pipeline failures and clean up temporary resources. Bind shell analysis and real script tests for whitespace paths, failed subprocesses and cleanup. Do not treat set -e alone as error-handling proof.","source_ids":["TECH-SRC-SHELLCHECK","TECH-SRC-BASH"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"],["test"]]},{"id":"TECH-JSON-001","version":"1","statement":"MUST: Record the consuming schema/parser contract. Validate syntax and required fields; reject duplicate keys in policy or security-sensitive inputs and avoid nonportable numeric assumptions. Bind schema/parser validation under a lint check; test changed loader behavior when executable parsing logic changes.","source_ids":["TECH-SRC-JSON"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"]]},{"id":"TECH-YAML-001","version":"1","statement":"MUST: Record parser/version and the consuming schema, including scalar-resolution behavior. Reject duplicate mapping keys, avoid executable object construction from untrusted input and validate required fields. Bind parser/schema lint and test changed loaders with ambiguous scalars or tags when relevant.","source_ids":["TECH-SRC-YAML"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"]]},{"id":"TECH-DOCKERFILE-001","version":"1","statement":"MUST: Record builder, target platform and trusted base-image digests with a reviewed update process. Keep build secrets out of arguments, layers and final images; minimize final contents and select least-privilege runtime users. Bind Dockerfile lint and checks that build and inspect the intended image; document justified runtime privilege requirements.","source_ids":["TECH-SRC-DOCKER","TECH-SRC-DOCKER-SECRETS"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"],["container"]]},{"id":"TECH-GITHUB-ACTIONS-001","version":"1","statement":"MUST: Record workflow triggers, approved runners and explicit token permissions. Pin external actions to reviewed immutable identities, keep untrusted event data out of shell interpolation and prevent privileged execution of untrusted changes. Bind workflow lint and negative tests for required-check/gate behavior; cancelled, missing or unjustifiably skipped required checks must not become success.","source_ids":["TECH-SRC-ACTIONS"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"],["test"]]},{"id":"TECH-WINDOWS-001","version":"1","statement":"MUST: Record supported Windows versions and architectures. Respect reserved names, case behavior, path/encoding and native process semantics. Bind tests on the promised native Windows environment covering affected path and failure behavior. A Linux container or WSL run alone is not native Windows acceptance evidence.","source_ids":["TECH-SRC-WINDOWS"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["test"]]},{"id":"TECH-LINUX-001","version":"1","statement":"MUST: Record supported Linux distributions or base images, architectures and required user-space dependencies. Handle case-sensitive paths, permissions, signals and process cleanup. Bind tests on the promised Linux environment; distinguish container user-space checks from host/kernel behavior requiring native validation.","source_ids":["TECH-SRC-LINUX"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["test"]]},{"id":"TECH-NODE-001","version":"1","statement":"MUST: Record Node.js, package-manager and module-system versions. Use reproducible dependency installation from the reviewed lockfile, handle asynchronous errors and validate process shutdown behavior. Bind runtime tests and dependency checks; test native addons on supported platform/runtime combinations when present.","source_ids":["TECH-SRC-NODE","TECH-SRC-ECMASCRIPT"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["test"],["dependency"]]},{"id":"TECH-DOTNET-001","version":"1","statement":"MUST: Record SDK and target-framework/runtime versions and supported operating systems. Restore reviewed dependency versions and preserve target-framework compatibility. Bind build, tests and dependency checks for the claimed targets; test platform-specific or native interop behavior on the affected targets.","source_ids":["TECH-SRC-DOTNET","TECH-SRC-CSHARP"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["build"],["test"],["dependency"]]},{"id":"TECH-JVM-001","version":"1","statement":"MUST: Record JDK/compiler and deployment JVM versions plus bytecode target. Use reviewed reproducible dependency resolution, preserve class-loading and public binary compatibility where promised and handle shutdown/resources. Bind build, tests and dependency checks on supported runtimes, including changed native interop.","source_ids":["TECH-SRC-JVM","TECH-SRC-JAVA"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["build"],["test"],["dependency"]]},{"id":"TECH-DOCKER-001","version":"1","statement":"MUST: Record container engine/target-platform and host assumptions. Run the built image with declared least privileges, external secret delivery and explicit persistent-data ownership. Bind image/container checks and start, readiness, shutdown and failure tests on the actual artifact; document host-dependent and recovery evidence separately.","source_ids":["TECH-SRC-DOCKER","TECH-SRC-DOCKER-SECRETS"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["container"],["test"]]},{"id":"TECH-REACT-001","version":"1","statement":"MUST: Record React and rendering-environment versions. Preserve component/Hook purity and Hook call rules; clean up effects and asynchronous work. Bind framework-aware lint and user-visible behavior tests covering affected loading, error and interaction states; preserve accessible semantics.","source_ids":["TECH-SRC-REACT","TECH-SRC-HTML"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"],["browser","test"]]},{"id":"TECH-NEXTJS-001","version":"1","statement":"MUST: Record Next.js version and selected router/runtime. Keep server-only secrets and dependencies across the correct server/client boundary, validate serialized boundary data and specify caching/authentication behavior. Bind a production build and route/interaction tests covering affected server, client and authorization cases.","source_ids":["TECH-SRC-NEXTJS","TECH-SRC-REACT"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["build"],["browser","test"]]},{"id":"TECH-FASTAPI-001","version":"1","statement":"MUST: Record FastAPI, Pydantic and ASGI/runtime versions. Validate request/response contracts, enforce authorization, handle dependency/lifespan cleanup and avoid blocking asynchronous handlers with unbounded synchronous work. Bind API and behavior tests for success, rejection and relevant persistence/lifespan failures using realistic dependencies where integration matters.","source_ids":["TECH-SRC-FASTAPI","TECH-SRC-PYTHON"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["api"],["test"]]}],"profiles":[{"id":"bash","version":"1","category":"shell","description":"Bash component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-BASH-001"],"quality_profiles":[],"recommendations":["Prefer ShellCheck with the declared shell dialect.","Keep shell adapters small; use Python for substantial shared cross-platform logic when practical."],"free_choices":["Control flow and helpers that preserve exit-status and argument semantics."]},{"id":"c","version":"1","category":"language","description":"C component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-C-001"],"quality_profiles":[],"recommendations":["Prefer bounded interfaces and one explicit resource-ownership convention.","Review full authorized CERT clauses before claiming clause conformance; only its publisher scope is recorded here."],"free_choices":["Data layout and algorithms within memory, ABI and platform constraints."]},{"id":"cpp","version":"1","category":"language","description":"C++ component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-CPP-001"],"quality_profiles":[],"recommendations":["Prefer standard ownership types and project-approved clang-format/clang-tidy settings.","GoogleTest is an optional framework; a C++17 project must select compatible guide rules and tool releases rather than adopting a living C++20 guide wholesale."],"free_choices":["Internal templates, algorithms and abstractions supported by the chosen compiler and error policy."]},{"id":"csharp","version":"1","category":"language","description":"C# component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-CSHARP-001"],"quality_profiles":[],"recommendations":["Prefer established Microsoft naming conventions and project-approved nullable analysis settings.","Propagate cancellation through operations that support cancellation."],"free_choices":["Internal types, records and decomposition when they preserve compatibility."]},{"id":"css","version":"1","category":"language","description":"CSS component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-CSS-001"],"quality_profiles":[],"recommendations":["Prefer established design tokens and component styles.","Treat the CSS snapshot as a standards inventory, not proof of browser support."],"free_choices":["Layout techniques, selectors and local styling choices that meet the contract."]},{"id":"docker","version":"1","category":"container","description":"Docker runtime component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-DOCKER-001"],"quality_profiles":[],"recommendations":["Prefer read-only filesystems and constrained resources when compatible with application needs.","Keep health/readiness checks aligned with actual service readiness."],"free_choices":["Image/runtime composition within the approved security, data and operating contract."]},{"id":"dockerfile","version":"1","category":"container","description":"Dockerfile component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-DOCKERFILE-001"],"quality_profiles":[],"recommendations":["Prefer multistage builds and a maintained minimal base appropriate to the application.","Use build-secret mounts where supported."],"free_choices":["Build-stage structure and caching strategy preserving reproducibility and secret boundaries."]},{"id":"dotnet","version":"1","category":"runtime","description":".NET component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-DOTNET-001"],"quality_profiles":[],"recommendations":["Use existing test-runner conventions and centrally reviewed dependency management where available."],"free_choices":["Internal assembly organization and test framework within the approved runtime contract."]},{"id":"fastapi","version":"1","category":"framework","description":"FastAPI component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-FASTAPI-001"],"quality_profiles":["python"],"recommendations":["Prefer dependency overrides for bounded unit/API tests and real infrastructure for critical integration contracts.","Keep schemas and documented API behavior synchronized."],"free_choices":["Internal dependency and service organization within the agreed API and lifecycle contracts."]},{"id":"github-actions","version":"1","category":"automation","description":"GitHub Actions component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-GITHUB-ACTIONS-001"],"quality_profiles":[],"recommendations":["Reuse the approved Backbone workflow contract and keep executable logic in reviewed scripts.","Prefer minimal job permissions and explicit shell selection."],"free_choices":["Job decomposition and safe parallelism within the existing runner and gate contracts."]},{"id":"go","version":"1","category":"language","description":"Go component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-GO-001"],"quality_profiles":[],"recommendations":["Prefer idiomatic small interfaces and explicit context propagation where cancellation is part of the contract.","Use go vet and race testing where supported; Effective Go alone is not the complete modern language specification."],"free_choices":["Package internals and concurrency mechanisms that satisfy the lifetime and correctness requirements."]},{"id":"html","version":"1","category":"language","description":"HTML component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-HTML-001"],"quality_profiles":[],"recommendations":["Use WCAG 2.2 AA as the default project accessibility target unless a reviewed project obligation requires another target.","Prefer native controls before custom interactive elements."],"free_choices":["Document composition and visual structure within semantics and accessibility constraints."]},{"id":"java","version":"1","category":"language","description":"Java component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-JAVA-001"],"quality_profiles":[],"recommendations":["Prefer the standard resource-management constructs and existing project patterns.","Google Java conventions are a candidate subset; do not import an incompatible language feature."],"free_choices":["Class decomposition and algorithms; interfaces are needed only when justified by the design."]},{"id":"javascript","version":"1","category":"language","description":"JavaScript component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-JAVASCRIPT-001"],"quality_profiles":[],"recommendations":["Prefer TypeScript for new application modules when the approved project architecture supports it; JavaScript remains supported.","Prefer established module and asynchronous patterns in the project."],"free_choices":["Internal helpers and algorithms, including async/await versus equivalent correctly handled promises."]},{"id":"json","version":"1","category":"format","description":"JSON component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-JSON-001"],"quality_profiles":[],"recommendations":["Use UTF-8 and a single consistent formatter.","Prefer explicit schemas for shared contracts."],"free_choices":["Object organization allowed by the authoritative schema."]},{"id":"jvm","version":"1","category":"runtime","description":"JVM component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-JVM-001"],"quality_profiles":[],"recommendations":["Keep compiler target and deployment runtime compatibility explicit.","Prefer the existing approved build tool."],"free_choices":["Module and package internals within the runtime and binary contract."]},{"id":"linux","version":"1","category":"platform","description":"Linux component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-LINUX-001"],"quality_profiles":[],"recommendations":["Prefer portable APIs and least-privilege execution.","Keep distro-specific assumptions documented."],"free_choices":["Internal adapters satisfying the actual distribution and kernel boundary."]},{"id":"nextjs","version":"1","category":"framework","description":"Next.js component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-NEXTJS-001"],"quality_profiles":[],"recommendations":["Prefer the existing router and deployment model; migrations require explicit planning.","Minimize client boundaries when behavior permits."],"free_choices":["Internal components and route implementation within the approved rendering and data contracts."]},{"id":"node","version":"1","category":"runtime","description":"Node.js component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-NODE-001"],"quality_profiles":[],"recommendations":["Prefer maintained runtime lines selected through reviewed updates.","Use existing project scripts for equivalent local and CI checks."],"free_choices":["Package internal organization and approved asynchronous patterns."]},{"id":"php","version":"1","category":"language","description":"PHP component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-PHP-001"],"quality_profiles":[],"recommendations":["Prefer current project conventions and typed public boundaries where supported.","Use a reviewed subset of PER Coding Style compatible with the selected PHP version."],"free_choices":["Internal class/function organization and approved framework patterns."]},{"id":"postgresql","version":"1","category":"database","description":"PostgreSQL component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-POSTGRESQL-001"],"quality_profiles":[],"recommendations":["Test migrations from representative prior schema/data as well as fresh installation.","Prefer reversible changes when safe; use reviewed forward recovery when reversing would lose data."],"free_choices":["Schema normalization and index designs within approved data contracts and measured performance requirements."]},{"id":"powershell","version":"1","category":"shell","description":"PowerShell component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-POWERSHELL-001"],"quality_profiles":[],"recommendations":["Prefer PSScriptAnalyzer and Pester or reviewed equivalent checks.","Keep platform adapters small and use Python for shared cross-platform automation logic when practical."],"free_choices":["Functions and parameter structure within the approved command and platform contract."]},{"id":"python","version":"1","category":"language","description":"Python component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-PYTHON-001"],"quality_profiles":["python"],"recommendations":["Prefer standard-library facilities and existing project conventions; document deviations through normal review.","Ruff, mypy and pytest are examples; use approved project equivalents when they establish the same obligations."],"free_choices":["Internal function decomposition and suitable algorithms within the accepted contracts."]},{"id":"react","version":"1","category":"framework","description":"React component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-REACT-001"],"quality_profiles":[],"recommendations":["Prefer existing component and state-management patterns.","Use effects for external synchronization rather than avoidable derived state."],"free_choices":["Component decomposition and local state choices consistent with the architectural boundaries."]},{"id":"sql","version":"1","category":"language","description":"SQL component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-SQL-001"],"quality_profiles":[],"recommendations":["Prefer constraints for database invariants and readable explicit queries.","Use PostgreSQL rules as an additional profile when PostgreSQL is the selected dialect."],"free_choices":["Equivalent query structure and indexing proposals supported by measured plans and correctness tests."]},{"id":"typescript","version":"1","category":"language","description":"TypeScript component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-TYPESCRIPT-001"],"quality_profiles":["typescript"],"recommendations":["Prefer explicit boundary types and narrowing over unchecked assertions.","Select one formatter and a compatible typed lint configuration."],"free_choices":["Internal inferred types, helper layout and algorithms consistent with the public contract."]},{"id":"windows","version":"1","category":"platform","description":"Windows component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-WINDOWS-001"],"quality_profiles":[],"recommendations":["Prefer portable path/process APIs and explicit text encodings.","Keep operating-system-specific handling isolated."],"free_choices":["Internal adapters compatible with the documented Windows support contract."]},{"id":"yaml","version":"1","category":"format","description":"YAML component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-YAML-001"],"quality_profiles":[],"recommendations":["Quote scalar values whose interpretation varies across approved consumers.","Prefer straightforward mappings over complex aliases when readability improves."],"free_choices":["Mapping layout allowed by the consumer contract."]}]}'
    roles = {'planner', 'implementer', 'reviewer', 'quality_checker', 'triage'}
    tasks = {'bugfix', 'implementation', 'architecture', 'review', 'documentation'}
    manifest_path = '.engineering-backbone/navigation.json'
    profile_path = '.engineering-backbone/quality-profile.json'
    workflows_path = '.engineering-backbone/workflows.json'
    missing = object()

    def fail(message):
        raise ValueError(message)

    def text(value, label, limit=4096):
        if (not isinstance(value, str) or not value.strip() or len(value) > limit
                or any(ord(c) < 32 or 127 <= ord(c) <= 159 for c in value)):
            fail('Invalid ' + label)
        value.encode('utf-8')
        return value

    def keys(value, names, label):
        if not isinstance(value, dict) or set(value) != set(names):
            fail(label + ' has missing or unknown keys')

    def identifier(value):
        if not isinstance(value, str) or re.fullmatch(r'[A-Za-z][A-Za-z0-9_.-]{0,63}', value) is None:
            fail('Invalid identifier')
        return value

    def sequence(value, label, *, nonempty=False, maximum=256):
        if (not isinstance(value, list) or len(value) > maximum
                or nonempty and not value):
            fail('Invalid ' + label)
        for item in value:
            text(item, label)
        if len(value) != len(set(value)):
            fail('Duplicate ' + label)
        return value

    def relative(value, *, anchor=False):
        value = text(value, 'relative path', 512)
        pieces = value.split('#')
        if len(pieces) > (2 if anchor else 1):
            fail('Unexpected path anchor')
        if anchor and len(pieces) == 2 and re.fullmatch(r'[a-z0-9][a-z0-9_-]*', pieces[1]) is None:
            fail('Anchor must be a lowercase portable Markdown heading ID')
        path = pieces[0]
        for part in path.split('/'):
            if (part in ('', '.', '..') or part[-1:] in ('.', ' ')
                    or any(c in part for c in '\\:<>"|?*')
                    or re.fullmatch(r'(?i)(?:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?', part)):
                fail('Unsafe or nonportable relative path')
        return path, pieces[1] if len(pieces) == 2 else None

    def scope_match(path, pattern):
        # Glob matching is segment-aware: * and ? never cross '/', while a
        # complete ** segment matches zero or more path segments.
        names, patterns = path.split('/'), pattern.split('/')

        @lru_cache(maxsize=None)
        def match(index, position):
            if position == len(patterns):
                return index == len(names)
            if patterns[position] == '**':
                return match(index, position + 1) or (
                    index < len(names) and match(index + 1, position))
            return index < len(names) and fnmatch.fnmatchcase(names[index], patterns[position]) and match(index + 1, position + 1)

        return match(0, 0)

    def linked(info):
        return stat.S_ISLNK(info.st_mode) or bool(
            getattr(info, 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0))

    def folder_path(value):
        value = Path(os.path.abspath(value))
        current = Path(value.anchor)
        for part in value.parts[1:]:
            current /= part
            info = current.lstat()
            if linked(info) or not stat.S_ISDIR(info.st_mode):
                fail('Root has symlink or non-directory ancestor')
        return value

    def locate(folder, name, *, optional=False):
        path, _ = relative(name)
        current = folder
        for index, part in enumerate(path.split('/')):
            if not current.is_dir():
                fail('Non-directory path ancestor')
            matches = [entry.name for entry in current.iterdir() if entry.name.casefold() == part.casefold()]
            if len(matches) > 1 or matches and matches[0] != part:
                fail('Case mismatch or ambiguous path: ' + name)
            current /= part
            try:
                info = current.lstat()
                mode = info.st_mode
            except FileNotFoundError:
                if optional:
                    return None
                fail('Required document or directory absent: ' + name)
            if linked(info):
                fail('Symlink in navigation path: ' + name)
            if index < len(path.split('/')) - 1 and not stat.S_ISDIR(mode):
                fail('Non-directory path ancestor')
        return current

    def read(folder, name, *, optional=False, limit=1048576):
        path = locate(folder, name, optional=optional)
        if path is None:
            return missing
        if not stat.S_ISREG(path.stat().st_mode) or path.stat().st_size > limit:
            fail('Nonregular or oversized navigation input: ' + name)
        data = path.read_bytes()
        if len(data) > limit:
            fail('Oversized navigation input: ' + name)
        return data

    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                fail('Duplicate JSON key')
            result[key] = value
        return result

    def decode(data):
        return json.loads(data.decode('utf-8'), object_pairs_hook=pairs,
                          parse_constant=lambda value: fail('Invalid JSON number'))

    def json_file(folder, name, *, optional=False):
        data = read(folder, name, optional=optional, limit=262144)
        return missing if data is missing else decode(data)

    def digest(value):
        return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                        separators=(',', ':')).encode('utf-8')).hexdigest()

    def document(folder, reference):
        name, anchor = relative(reference, anchor=True)
        data = read(folder, name)
        content = data.decode('utf-8')
        if not content.strip() or '\x00' in content:
            fail('Empty or invalid navigation document: ' + name)
        if anchor:
            # Deliberately narrow heading convention; arbitrary HTML IDs, Setext
            # headings and renderer-specific punctuation are not assumed.
            headings, counts, fenced = set(), {}, False
            for line in content.splitlines():
                if re.match(r'^\s*(```|~~~)', line):
                    fenced = not fenced
                    continue
                match = re.match(r'^ {0,3}#{1,6} ([A-Za-z0-9 _-]+?)(?: +#+)?\s*$', line)
                if match and not fenced:
                    slug = match[1].strip().lower().replace(' ', '-')
                    count = counts.get(slug, 0)
                    counts[slug] = count + 1
                    headings.add(slug + ('-' + str(count) if count else ''))
            if anchor not in headings:
                fail('Missing or unsupported Markdown heading anchor: ' + reference)
        return {'path': reference, 'sha256': hashlib.sha256(data).hexdigest()}

    def package(folder, catalog):
        prefix = 'standards/technologies' if source else '.engineering-backbone/standards/technologies'
        for name in ('sources', 'rules'):
            wanted = {'schema_version': '1', 'version': catalog['version'], name: catalog[name]}
            if json_file(folder, prefix + '/' + name + '.json') != wanted:
                fail('Managed technology ' + name + ' differs from trusted authority')
        directory = locate(folder, prefix + '/profiles')
        if not directory.is_dir():
            fail('Technology profiles path is not a directory')
        actual = {path.name for path in directory.iterdir()}
        if actual != {entry['id'] + '.json' for entry in catalog['profiles']}:
            fail('Managed technology profile set differs from trusted authority')
        for entry in catalog['profiles']:
            if json_file(folder, prefix + '/profiles/' + entry['id'] + '.json') != entry:
                fail('Managed technology profile differs from trusted authority')
        return prefix

    def effective_workflow(folder, approved_root=None):
        value = json_file(folder, workflows_path, optional=True)
        if not isinstance(value, dict):
            return value

        def check_map(workflow):
            result = {}
            for check in workflow.get('checks', []):
                if not isinstance(check, dict) or check.get('id') in result:
                    fail('Malformed or duplicate workflow check')
                result[check.get('id')] = check
            return result

        current = check_map(value)
        if approved_root is None:
            return value
        approved = json_file(approved_root, workflows_path, optional=True)
        if not isinstance(approved, dict) or approved.get('enabled') is not True:
            return value
        approved_checks = check_map(approved)
        # Match workflow preparation: an existing ID executes the full approved
        # definition. Only genuinely new IDs retain candidate definitions.
        return dict(value, checks=[approved_checks.get(key, check)
                                   for key, check in current.items()])

    def manifest(folder, catalog, *, complete=False, approved_root=None):
        value = json_file(folder, manifest_path, optional=True)
        if value is missing:
            return None
        keys(value, {'schema_version', 'enabled', 'documents', 'always', 'roles', 'tasks', 'components'},
             'Navigation manifest')
        if value['schema_version'] != '1' or type(value['enabled']) is not bool:
            fail('Invalid navigation schema or activation flag')
        package(folder, catalog)
        documents = value['documents']
        if not isinstance(documents, dict) or len(documents) > 256:
            fail('Invalid navigation documents')
        for key, reference in documents.items():
            identifier(key)
            document(folder, reference)

        def refs(items):
            sequence(items, 'document references')
            if set(items) - set(documents):
                fail('Unknown navigation document ID')

        refs(value['always'])
        for field, names in (('roles', roles), ('tasks', tasks)):
            keys(value[field], names, 'Navigation ' + field)
            for items in value[field].values():
                refs(items)
        components = value['components']
        if not isinstance(components, list) or len(components) > 256:
            fail('Invalid components')
        profiles = {item['id']: item for item in catalog['profiles']}
        rules = {item['id']: item for item in catalog['rules']}
        found = set()
        quality = json_file(folder, profile_path, optional=True)
        workflow = effective_workflow(folder, approved_root)
        active = complete or value['enabled']
        if active and (not isinstance(quality, dict) or quality.get('enabled') is not True
                       or not isinstance(workflow, dict) or workflow.get('enabled') is not True):
            fail('Active navigation requires active quality and workflow profiles')
        checks = {}
        if isinstance(workflow, dict):
            for check in workflow.get('checks', []):
                if not isinstance(check, dict) or check.get('id') in checks:
                    fail('Malformed or duplicate workflow check')
                checks[check.get('id')] = check
        for component in components:
            keys(component, {'id', 'paths', 'profiles', 'documents', 'checks'}, 'Component')
            key = identifier(component['id'])
            if key in found:
                fail('Duplicate component ID')
            found.add(key)
            sequence(component['paths'], 'component paths', nonempty=True)
            for path in component['paths']:
                relative(path)
                locate(folder, path, optional=True)
            sequence(component['profiles'], 'technology profiles', nonempty=True)
            if set(component['profiles']) - set(profiles):
                fail('Unknown technology profile')
            refs(component['documents'])
            selected = {rule for profile in component['profiles'] for rule in profiles[profile]['rules']}
            required_quality = {profile for name in component['profiles'] for profile in profiles[name]['quality_profiles']}
            if active and required_quality - set(quality.get('profiles', [])):
                fail('Required quality profile missing for technology component')
            bindings = component['checks']
            if not isinstance(bindings, list) or len(bindings) > 256:
                fail('Invalid component check bindings')
            bound = {}
            for binding in bindings:
                keys(binding, {'rule_id', 'check_ids'}, 'Technology check binding')
                rule = identifier(binding['rule_id'])
                if rule not in selected or rule in bound:
                    fail('Unknown, unselected or duplicate technology rule binding')
                sequence(binding['check_ids'], 'technology check IDs', nonempty=True, maximum=100)
                for check in binding['check_ids']:
                    identifier(check)
                    if check not in checks or 'pr' not in checks[check].get('phases', []):
                        fail('Technology check binding must reference a PR workflow check')
                bound[rule] = binding['check_ids']
            if active:
                for rule in selected:
                    covered = {checks[key].get('kind') for key in bound.get(rule, [])}
                    if any(not covered.intersection(group) for group in rules[rule]['check_kind_groups']):
                        fail('Required technology check-kind coverage missing: ' + rule)
        if active and not components:
            fail('Active navigation requires mapped components')
        return value

    def inherited(candidate, base):
        if base is None or not base['enabled']:
            return
        if candidate is None or not candidate['enabled']:
            fail('Active navigation cannot be removed or disabled')
        if any(candidate['documents'].get(key) != value for key, value in base['documents'].items()):
            fail('Inherited navigation document targets cannot be removed or remapped')
        for field in ('always',):
            if set(base[field]) - set(candidate[field]):
                fail('Inherited mandatory document route cannot be removed')
        for field in ('roles', 'tasks'):
            for route in base[field]:
                if set(base[field][route]) - set(candidate[field][route]):
                    fail('Inherited role or task document route cannot be removed')
        current = {item['id']: item for item in candidate['components']}
        for previous in base['components']:
            now = current.get(previous['id'])
            if now is None:
                fail('Inherited component cannot be removed')
            for field in ('paths', 'profiles', 'documents'):
                if set(previous[field]) - set(now[field]):
                    fail('Inherited component routing cannot be weakened')
            bindings = {item['rule_id']: set(item['check_ids']) for item in now['checks']}
            for binding in previous['checks']:
                if set(binding['check_ids']) - bindings.get(binding['rule_id'], set()):
                    fail('Inherited technology check bindings cannot be removed')

    try:
        root = folder_path(root)
        catalog = decode(technology_catalog_json.encode('utf-8'))
        keys(catalog, {'version', 'sources', 'rules', 'profiles'}, 'Trusted technology catalog')
        if not isinstance(catalog['version'], str):
            fail('Invalid trusted technology catalog version')
        for section in ('sources', 'rules', 'profiles'):
            if not isinstance(catalog[section], list) or not 1 <= len(catalog[section]) <= 256:
                fail('Invalid trusted technology catalog section')
            identifiers = [identifier(item['id']) for item in catalog[section]]
            if len(identifiers) != len(set(identifiers)):
                fail('Duplicate trusted technology identity')
        if source:
            package(root, catalog)
        if trusted_base is not None:
            trusted_base = folder_path(trusted_base)
        candidate = manifest(root, catalog, approved_root=trusted_base)
        if trusted_base is not None:
            # A legacy approved base without navigation has no extension package.
            base = manifest(trusted_base, catalog)
            inherited(candidate, base)
            if candidate is not None and candidate['enabled'] and (base is None or not base['enabled']):
                if base is None:
                    fail('Navigation activation requires an already reviewed inactive seed')
                manifest(trusted_base, catalog, complete=True)
                if candidate != dict(base, enabled=True):
                    fail('Navigation activation must match the reviewed seed except enabled')
        if request is None:
            if expected is not None:
                fail('Handoff verification requires a request')
            return {'errors': [], 'context': None}
        if candidate is None or not candidate['enabled']:
            fail('Context resolution requires active navigation')
        keys(request, {'schema_version', 'task_packet', 'task_type', 'paths', 'components', 'revision'},
             'Navigation request')
        if request['schema_version'] != '1' or request['task_type'] not in tasks:
            fail('Invalid navigation request version or task type')
        if not isinstance(request['revision'], str) or re.fullmatch(r'[0-9a-f]{40}', request['revision']) is None:
            fail('Request revision must be a full lowercase commit SHA')
        relative(request['task_packet'])
        packet = json_file(root, request['task_packet'])
        packet_keys = {'schema_version', 'id', 'title', 'objective', 'role', 'risk', 'repository',
                       'approved_sources', 'scope', 'acceptance', 'validation', 'execution_budget',
                       'stop_conditions', 'forbidden_actions', 'status'}
        keys(packet, packet_keys, 'Task Packet')
        if packet['schema_version'] != '1' or packet['role'] not in roles:
            fail('Invalid Task Packet version or role')
        for field in ('id', 'title', 'objective'):
            text(packet[field], 'Task Packet ' + field)
        if packet['risk'] not in {'low', 'medium', 'high', 'critical'}:
            fail('Invalid Task Packet risk')
        if packet['status'] not in {'planned', 'active', 'blocked', 'ready_for_review', 'completed'}:
            fail('Invalid Task Packet status')
        keys(packet['validation'], {'commands', 'manual_evidence'}, 'Task Packet validation')
        for entries in packet['validation'].values():
            sequence(entries, 'Task Packet validation entries')
        keys(packet['execution_budget'], {'max_iterations'}, 'Task Packet execution budget')
        budget = packet['execution_budget']['max_iterations']
        if type(budget) is not int or not 1 <= budget <= 10:
            fail('Invalid Task Packet execution budget')
        acceptance = packet['acceptance']
        if not isinstance(acceptance, list) or not 1 <= len(acceptance) <= 256:
            fail('Invalid Task Packet acceptance')
        acceptance_ids = set()
        for criterion in acceptance:
            keys(criterion, {'id', 'description', 'verification', 'status', 'evidence'},
                 'Task Packet acceptance criterion')
            text(criterion['id'], 'acceptance ID')
            text(criterion['description'], 'acceptance description')
            if criterion['id'] in acceptance_ids:
                fail('Duplicate Task Packet acceptance ID')
            acceptance_ids.add(criterion['id'])
            if criterion['verification'] not in {'automatic', 'manual', 'hybrid'}:
                fail('Invalid Task Packet verification')
            if criterion['status'] not in {'pending', 'pass', 'fail', 'blocked'}:
                fail('Invalid Task Packet acceptance status')
            sequence(criterion['evidence'], 'acceptance evidence', nonempty=criterion['status'] == 'pass')
            if packet['status'] == 'completed' and criterion['status'] != 'pass':
                fail('Completed Task Packet has unresolved acceptance')
        keys(packet['scope'], {'include', 'exclude'}, 'Task Packet scope')
        for field in ('include', 'exclude'):
            sequence(packet['scope'][field], 'task scope', nonempty=field == 'include')
            for pattern in packet['scope'][field]:
                text(pattern, 'Task Packet scope pattern', 512)
                if (pattern.startswith('/') or '\\' in pattern or ':' in pattern
                        or any(part in ('', '.', '..') for part in pattern.split('/'))):
                    fail('Invalid Task Packet scope pattern')
        for field in ('stop_conditions', 'forbidden_actions', 'approved_sources'):
            sequence(packet[field], field, nonempty=True)
        repository = packet['repository']
        keys(repository, {'base_branch', 'base_revision', 'head_revision'}, 'Task Packet repository')
        branch = text(repository['base_branch'], 'Task Packet base branch')
        if (branch == 'HEAD' or branch.startswith(('-', '/', '.')) or branch.endswith(('/', '.'))
                or any(char.isspace() or char in '~^:?*[\\' for char in branch)
                or any(part.startswith('.') or part.endswith('.lock') for part in branch.split('/'))
                or any(value in branch for value in ('..', '//', '@{'))):
            fail('Invalid Task Packet base branch')
        for field in ('base_revision', 'head_revision'):
            revision = repository[field]
            required = packet['status'] in {'completed', 'ready_for_review'} or (
                packet['status'] == 'active' and packet['role'] == 'reviewer')
            if revision is None and not required:
                continue
            if not isinstance(revision, str) or re.fullmatch(r'[0-9a-f]{40}', revision) is None:
                fail('Invalid or missing Task Packet revision')
        if repository['head_revision'] is not None and repository['head_revision'] != request['revision']:
            fail('Request revision differs from Task Packet reviewed head')
        if packet['role'] == 'reviewer' and repository['head_revision'] is None:
            fail('Reviewer context requires a frozen Task Packet head')
        sequence(request['paths'], 'request paths')
        sequence(request['components'], 'request component IDs')
        if not request['paths'] and not request['components']:
            fail('Request needs affected paths or named components')
        mapped = {item['id']: item for item in candidate['components']}
        if set(request['components']) - set(mapped):
            fail('Unknown requested component')
        selected = set(request['components'])
        includes, excludes = packet['scope']['include'], packet['scope']['exclude']
        for path in request['paths']:
            relative(path)
            located = locate(root, path, optional=True)
            directory_request = located is not None and located.is_dir()
            if (not any(scope_match(path, pattern) for pattern in includes)
                    or any(scope_match(path, pattern) or directory_request and pattern == path + '/**'
                           for pattern in excludes)):
                fail('Requested path is outside Task Packet authorized scope')
            matches = {key for key, item in mapped.items()
                       if any(path == prefix or path.startswith(prefix + '/')
                              or directory_request and prefix.startswith(path + '/') for prefix in item['paths'])}
            if not matches:
                fail('Requested path has no component route')
            selected.update(matches)
        # A named component must intersect declared task scope. Exact paths are
        # still the authorization boundary; this does not authorize its subtree.
        for key in request['components']:
            if not any(any(scope_match(prefix, pattern) or pattern.startswith(prefix + '/')
                           or scope_match(prefix + '/_navigation_scope_probe_', pattern)
                           for pattern in includes)
                       and not any(scope_match(prefix, pattern) or pattern == prefix + '/**' for pattern in excludes)
                       for prefix in mapped[key]['paths']):
                fail('Named component is outside Task Packet scope')
        quality = json_file(root, profile_path)
        workflow = effective_workflow(root, trusted_base)
        references = set(candidate['always']) | set(candidate['roles'][packet['role']]) | set(candidate['tasks'][request['task_type']])
        selected_profiles, technology_bindings = set(), {}
        for key in sorted(selected):
            item = mapped[key]
            references.update(item['documents'])
            selected_profiles.update(item['profiles'])
            technology_bindings[key] = item['checks']
        paths = {candidate['documents'][key] for key in references}
        paths.update({manifest_path, profile_path, workflows_path, request['task_packet']})
        prefix = 'standards' if source else '.engineering-backbone/standards'
        paths.update({prefix + '/sources.json', prefix + '/rules.json',
                      prefix + '/technologies/sources.json', prefix + '/technologies/rules.json'})
        paths.update(prefix + '/profiles/' + key + '.json' for key in quality['profiles'])
        paths.update(prefix + '/technologies/profiles/' + key + '.json' for key in selected_profiles)
        paths.update(path for path in quality['documents'].values() if path)
        paths.update({'policy/core.md', 'policy/core.json', 'policy/quality.md', 'docs/quality/README.md',
                      'docs/quality/technology-profiles.md', 'docs/agent-navigation.md'} if source else
                     {'.engineering-backbone/core.md', '.engineering-backbone/core.json',
                      '.engineering-backbone/project.json', '.engineering-backbone/quality-policy.md',
                      '.engineering-backbone/quality-guide.md', '.engineering-backbone/technology-guide.md',
                      '.engineering-backbone/navigation-guide.md'})
        for name in ('AGENTS.md', 'CONTRIBUTING.md', '.github/copilot-instructions.md'):
            if locate(root, name, optional=True) is not None:
                paths.add(name)
        directories = {''}
        instruction_scopes = list(request['paths'])
        instruction_scopes.extend(prefix for key in request['components'] for prefix in mapped[key]['paths'])
        visited = 0
        for path in instruction_scopes:
            located = locate(root, path, optional=True)
            is_directory = located is not None and located.is_dir()
            parts = path.split('/') if is_directory else path.split('/')[:-1]
            directories.update('/'.join(parts[:index]) for index in range(1, len(parts) + 1))
            if is_directory:
                # Directory/component requests include all descendant instruction
                # scopes. File requests include their ancestors. Bound traversal
                # and refuse symlink subtrees instead of silently missing rules.
                def discovery_error(error):
                    raise error

                for current, subdirectories, files in os.walk(located, followlinks=False, onerror=discovery_error):
                    visited += 1
                    if visited > 4096:
                        fail('Instruction discovery exceeds directory limit; narrow request paths')
                    for child in subdirectories:
                        if linked((Path(current) / child).lstat()):
                            fail('Symlink subtree during instruction discovery')
                    directories.add(Path(current).relative_to(root).as_posix())
        for directory in sorted(directories):
            prefix_path = directory + '/' if directory else ''
            for filename in ('AGENTS.md', 'AGENTS.override.md'):
                name = prefix_path + filename
                if locate(root, name, optional=True) is not None:
                    if filename == 'AGENTS.override.md':
                        fail('Unresolved instruction override requires explicit reconciliation')
                    paths.add(name)
        rule_map = {item['id']: item for item in catalog['rules']}
        profile_map = {item['id']: item for item in catalog['profiles']}
        selected_rules = {rule for name in selected_profiles for rule in profile_map[name]['rules']}
        selected_check_ids = {check for bindings in technology_bindings.values()
                              for binding in bindings for check in binding['check_ids']}
        selected_check_ids.update(check for binding in quality['checks'] for check in binding['check_ids'])
        if not isinstance(authority, dict):
            fail('Context resolution requires compiler-owned core authority')
        core_rules, core_profiles = authority['rules'], authority['profiles']
        core_profile_map = {item['id']: item for item in core_profiles}
        core_rule_map = {item['id']: item for item in core_rules}
        selected_core_rules = {rule for key in quality['profiles'] for rule in core_profile_map[key]['rules']}
        context = {
            'schema_version': '1', 'claim': 'structural-context-only',
            'revision': request['revision'], 'task_id': packet['id'], 'role': packet['role'],
            'request_sha256': digest(request), 'navigation_sha256': digest(candidate),
            'quality_profile_sha256': digest(quality), 'backbone_ref': quality['backbone_ref'],
            'quality_catalog_version': quality['catalog_version'],
            'technology_catalog_version': catalog['version'], 'technology_catalog_sha256': digest(catalog),
            'components': sorted(selected),
            'technology_profiles': [{'id': key, 'version': profile_map[key]['version']} for key in sorted(selected_profiles)],
            'technology_rules': [{'id': key, 'version': rule_map[key]['version']} for key in sorted(selected_rules)],
            'technology_check_bindings': technology_bindings,
            'quality_profiles': [{'id': key, 'version': core_profile_map[key]['version']} for key in sorted(quality['profiles'])],
            'quality_rules': [{'id': key, 'version': core_rule_map[key]['version']} for key in sorted(selected_core_rules)],
            'quality_check_bindings': quality['checks'],
            'checks': sorted((item for item in workflow['checks'] if item['id'] in selected_check_ids), key=lambda item: item['id']),
            'documents': [document(root, reference) for reference in sorted(paths)],
            'runtime_loading': 'unverified',
        }
        context['context_sha256'] = digest(context)
        if expected is not None and expected != context:
            fail('Handoff context differs from recomputed snapshot')
        return {'errors': [], 'context': context}
    except (ValueError, OSError, UnicodeError, KeyError, TypeError, RecursionError) as exc:
        return {'errors': ['Navigation: ' + str(exc)], 'context': None}
