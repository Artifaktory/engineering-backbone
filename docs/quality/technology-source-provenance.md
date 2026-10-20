# Technology source provenance

Observed **2026-10-14** through the primary publisher pages below. The exact
machine-readable identities, editions and inspected scope are in
`.engineering-backbone/standards/technologies/sources.json`. All `TECH-*` statements are our own
component requirements. A source reference is not wholesale adoption, a tool
installation claim or certification. Existing ISO/IEC provenance remains in the
unchanged core catalog.

| Source | Selected scope and boundary |
|---|---|
| [Python PEP 8](https://peps.python.org/pep-0008/) and [PEP 257](https://peps.python.org/pep-0257/) | Project consistency, interfaces and documentation; typing/test requirements are our additional decisions. |
| [TC39 control abstraction objects](https://tc39.es/ecma262/multipage/control-abstraction-objects.html) | Promise states in the living draft titled ECMAScript 2027; no automatic target upgrade. |
| [TypeScript strict](https://www.typescriptlang.org/tsconfig/strict.html) | Strict compiler-check family; actual compiler version/configuration remains explicit. |
| [Google Java](https://google.github.io/styleguide/javaguide.html) | Style conventions selected for compatibility, not automatic full-guide adoption. |
| [Microsoft C# conventions](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions) | Project coding consistency; .NET targets remain project-owned. |
| [Effective Go](https://go.dev/doc/effective_go) | Formatting, errors and concurrency guidance; not a comprehensive current-language specification. |
| [SEI CERT C publisher page](https://www.sei.cmu.edu/library/sei-cert-c-coding-standard-rules-for-developing-safe-reliable-and-secure-systems-2016-edition/) | **Public scope only.** The 2016 full-text link redirected to registration and the wiki did not load. No CERT clause-level adoption or verification is claimed. |
| [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) and [Google C++](https://google.github.io/styleguide/cppguide.html) | Resource/interface guidance and self-contained headers. Google currently targets C++20. The project must reconcile version and exception-policy differences. |
| [GoogleTest Primer](https://google.github.io/googletest/primer.html) | Optional assertion/fixture framework example, not a coding standard. |
| [PHP-FIG PER Coding Style](https://www.php-fig.org/per/coding-style/) | Page observed as version 3.1; actual compatible subset must be selected. |
| [WHATWG HTML](https://html.spec.whatwg.org/multipage/dom.html) | Semantic elements and content models; living publication observation, not a browser matrix. |
| [W3C CSS Snapshot 2026](https://www.w3.org/TR/2026/NOTE-css-2026-20260622/) and [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | CSS specification inventory and accessibility criteria; browser compatibility and manual accessibility evidence remain necessary. |
| [PostgreSQL 18 SQL syntax](https://www.postgresql.org/docs/18/sql-syntax.html), [constraints](https://www.postgresql.org/docs/18/ddl-constraints.html), [query parameters](https://www.postgresql.org/docs/18/libpq-exec.html), [isolation](https://www.postgresql.org/docs/18/transaction-iso.html), [backup](https://www.postgresql.org/docs/18/backup.html) | Reviewed documented concepts; version 18 is the source edition, not an assumption about Artifaktory/Tars deployment. Migration/recovery criteria are project obligations. |
| [PowerShell 7.5 error handling](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally?view=powershell-7.5) | Terminating errors and cleanup; native exit status needs separate checking. |
| [PSScriptAnalyzer](https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/overview?view=ps-modules) and [Pester](https://pester.dev/docs/quick-start) | Optional configurable static and executable check tools. |
| [ShellCheck SC2086](https://www.shellcheck.net/wiki/SC2086) | Quoting, word splitting and glob behavior. |
| [GNU Bash manual](https://www.gnu.org/software/bash/manual/bash.html) | **Indexed summary only.** Repeated direct publisher fetches timed out; no full manual section adoption claimed. Shell obligations are organization-owned, with independently retrieved ShellCheck support. |
| [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259) and [YAML 1.2.2](https://yaml.org/spec/1.2.2/) | Syntax, keys and representation concerns; actual consumer-parser semantics must be tested. |
| [GitHub workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) | Events, permissions, conditions and shell syntax; gate negative tests are our own requirement. |
| [Docker build practices](https://docs.docker.com/build/building/best-practices/) and [build secrets](https://docs.docker.com/build/building/secrets/) | Base images, image contents and secret delivery; runtime evidence remains project-specific. |
| [Windows paths](https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file) and [Linux user-space API](https://docs.kernel.org/userspace-api/index.html) | Platform constraints/scope; actual supported platforms and native tests must be declared and executed. |
| [Node errors](https://nodejs.org/api/errors.html), [.NET testing](https://learn.microsoft.com/en-us/dotnet/core/testing/) and [JVM SE21](https://docs.oracle.com/javase/specs/jvms/se21/html/index.html) | Runtime/error/test concepts; no source-display version becomes a required runtime. |
| [React rules](https://react.dev/reference/rules), [Next.js boundaries](https://nextjs.org/docs/app/getting-started/server-and-client-components), [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/) | Framework-specific boundaries and testing guidance; real framework versions, authorization and integrations need project evidence. |

Living-page observations are dated. The reviewed Backbone revision fixes the
selected organization-owned rules; a future website edit does not change those
rules. No upstream text snapshot or licensed normative text is redistributed.
Updating an edition or broadening adoption requires a reviewed source change,
compatibility checks and explicit project uptake.
