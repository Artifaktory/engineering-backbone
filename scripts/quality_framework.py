#!/usr/bin/env python3
"""Trusted structural quality-profile guard; it never runs project commands.

The compiler embeds the exact self-contained ``quality_errors`` function and its
reviewed catalog in the validator/workflow. Candidate Python, schemas and catalog
files are input data and cannot supply authority.
"""


def quality_errors(root, trusted_base=None, *, source=False):
    """Return bounded contract errors, not semantic approval or certification."""
    import csv
    from datetime import date
    import io
    import json
    import os
    from pathlib import Path
    import re
    import stat

    catalog_json = '{"version":"1.0.0","sources":[{"id":"SRC-ISO-25010","title":"ISO/IEC 25010 product quality model","edition":"2023, edition 2","url":"https://www.iso.org/standard/78176.html","status":"published","access":"public-scope-only","adoption":"reference-only","verified_sections":["Official edition and public description of product quality evaluation; no full normative clauses reviewed."]},{"id":"SRC-ISO-12207","title":"ISO/IEC/IEEE 12207 software life cycle processes","edition":"2026, edition 2","url":"https://www.iso.org/standard/90219.html","status":"published","access":"public-scope-only","adoption":"reference-only","verified_sections":["Official edition and public lifecycle scope; no full normative clauses reviewed."]},{"id":"SRC-ISO-29148","title":"ISO/IEC/IEEE 29148 requirements engineering","edition":"2018, edition 2","url":"https://www.iso.org/standard/72089.html","status":"published","access":"public-scope-only","adoption":"reference-only","verified_sections":["Official published edition and public requirements scope; a revision draft is separate; no full normative clauses reviewed."]},{"id":"SRC-ISO-42010","title":"ISO/IEC/IEEE 42010 architecture description","edition":"2022, edition 2","url":"https://www.iso.org/standard/74393.html","status":"published","access":"public-scope-only","adoption":"reference-only","verified_sections":["Official edition and public architecture-description scope; no full normative clauses reviewed."]},{"id":"SRC-ISO-29119-2","title":"ISO/IEC/IEEE 29119-2 test processes","edition":"2021, edition 2","url":"https://www.iso.org/standard/79428.html","status":"published","access":"public-scope-only","adoption":"reference-only","verified_sections":["Official edition and public test-process scope; no full normative clauses reviewed."]},{"id":"SRC-ISO-29119-3","title":"ISO/IEC/IEEE 29119-3 test documentation","edition":"2021, edition 2","url":"https://www.iso.org/standard/79429.html","status":"published","access":"public-scope-only","adoption":"reference-only","verified_sections":["Official edition and public test-documentation scope; no normative templates or full clauses adopted."]},{"id":"SRC-MICROSOFT-SDL","title":"Microsoft SDL public practices","edition":"Living guidance observed 2026-10-13","url":"https://www.microsoft.com/en-us/securityengineering/sdl/practices","status":"living-guidance","access":"public-guidance","adoption":"public-guidance","verified_sections":["Public descriptions of security governance, threat analysis and security verification activities."]},{"id":"SRC-GOOGLE-CPP","title":"Google C++ Style Guide","edition":"Living guidance observed 2026-10-13; targets C++20","url":"https://google.github.io/styleguide/cppguide.html","status":"living-guidance","access":"public-guidance","adoption":"reference-only","verified_sections":["Public language-target description and readability/consistency guidance; C++17 compatibility subset not adopted."]},{"id":"SRC-CODEX-INSTRUCTIONS","title":"Codex project instruction discovery","edition":"Living guidance observed 2026-10-13","url":"https://learn.chatgpt.com/docs/agent-configuration/agents-md","status":"living-guidance","access":"public-guidance","adoption":"public-guidance","verified_sections":["Public discovery and override behavior; intended-client loading still requires project verification."]},{"id":"SRC-COPILOT-INSTRUCTIONS","title":"GitHub Copilot instruction support","edition":"Living guidance observed 2026-10-13","url":"https://docs.github.com/en/copilot/reference/custom-instructions-support","status":"living-guidance","access":"public-guidance","adoption":"public-guidance","verified_sections":["Public support matrix for instruction types and clients; intended-client loading still requires project verification."]},{"id":"SRC-IEC-61508","title":"IEC 61508-3 safety-related software","edition":"2010, edition 2","url":"https://webstore.iec.ch/en/publication/5517","status":"published","access":"public-scope-only","adoption":"reference-only","verified_sections":["Official edition and public safety-related software scope; full text, applicability and certification scheme unreviewed."]},{"id":"SRC-IEC-62304","title":"IEC 62304 medical device software lifecycle","edition":"2006 plus amendment 1:2015, consolidated edition 1.1","url":"https://webstore.iec.ch/en/publication/22794","status":"published","access":"public-scope-only","adoption":"reference-only","verified_sections":["Official consolidated edition and public medical-device software scope; full text, applicability and certification scheme unreviewed."]}],"rules":[{"id":"QUAL-REQ-001","version":"1","statement":"Before non-trivial work, record identified requirements, measurable quality goals, material risks and verifiable acceptance criteria. Map each selected quality rule to project requirements or risks and its planned evidence.","source_ids":["SRC-ISO-25010","SRC-ISO-29148"],"source_alignment":"Organization-owned requirement informed by the referenced public scopes; no normative clause conformance claimed.","responsibilities":["planner","reviewer"],"phases":["planning"],"verification":"manual","artifacts":["quality_plan","traceability"],"check_kind_groups":[],"waivable":false},{"id":"QUAL-DES-001","version":"1","statement":"Before a material design or implementation change, document affected interfaces, architectural decisions, quality consequences and security assumptions. Obtain independent plan/design review proportional to risk; preserve existing architecture locations.","source_ids":["SRC-ISO-42010","SRC-MICROSOFT-SDL"],"source_alignment":"Organization-owned requirement informed by the referenced public scopes; no normative clause conformance claimed.","responsibilities":["planner","reviewer"],"phases":["planning","design"],"verification":"manual","artifacts":["quality_plan","traceability"],"check_kind_groups":[],"waivable":false},{"id":"QUAL-CODE-001","version":"1","statement":"Apply the project-selected language, coding and security rules to changed code. Review suitability, correctness and maintainability; run the applicable compiler, lint and analysis checks without weakening inherited controls.","source_ids":["SRC-ISO-25010","SRC-MICROSOFT-SDL"],"source_alignment":"Organization-owned requirement informed by the referenced public scopes; no normative clause conformance claimed.","responsibilities":["implementer","quality_checker","reviewer"],"phases":["implementation","verification"],"verification":"hybrid","artifacts":["quality_plan","traceability"],"check_kind_groups":[],"waivable":false},{"id":"QUAL-TEST-001","version":"1","statement":"Define risk-based tests for affected requirements and critical behavior, including relevant success, rejection, boundary and failure cases. Add meaningful regression coverage for reproducible fixes. Record automated and manual coverage and unresolved gaps.","source_ids":["SRC-ISO-29119-2","SRC-ISO-29119-3"],"source_alignment":"Organization-owned requirement informed by the referenced public scopes; no normative clause conformance claimed.","responsibilities":["planner","implementer","quality_checker","reviewer"],"phases":["planning","implementation","verification"],"verification":"hybrid","artifacts":["test_strategy","traceability"],"check_kind_groups":[["test","docs"]],"waivable":false},{"id":"QUAL-DOC-001","version":"1","statement":"Update affected requirement, design, user and operational documentation when behavior, contracts or operation change. Trace the impact or a justified no-impact decision without duplicating established authoritative documents.","source_ids":["SRC-ISO-29148","SRC-ISO-42010"],"source_alignment":"Organization-owned requirement informed by the referenced public scopes; no normative clause conformance claimed.","responsibilities":["implementer","reviewer"],"phases":["implementation","review"],"verification":"manual","artifacts":["quality_plan","traceability"],"check_kind_groups":[],"waivable":false},{"id":"QUAL-EVID-001","version":"1","statement":"Bind actual check and review results to the inspected revision and record commands, exit codes, acceptance coverage and limitations. Keep unexecuted, failed and blocked evidence visible; declarations, generated reports and structural validation are not runtime proof.","source_ids":["SRC-ISO-12207","SRC-ISO-29119-3"],"source_alignment":"Organization-owned requirement informed by the referenced public scopes; no normative clause conformance claimed.","responsibilities":["quality_checker","reviewer"],"phases":["verification","review","publication"],"verification":"manual","artifacts":["traceability"],"check_kind_groups":[],"waivable":false},{"id":"QUAL-REVIEW-001","version":"1","statement":"Obtain independent review of one frozen base/head/patch snapshot after required checks. Triage before repairs; repair confirmed findings and review their Delta and direct regressions. Preserve human approvals, existing gates and stop conditions.","source_ids":["SRC-ISO-12207"],"source_alignment":"Organization-owned requirement informed by the referenced public scopes; no normative clause conformance claimed.","responsibilities":["reviewer","triage","implementer","quality_checker"],"phases":["review","publication"],"verification":"manual","artifacts":["quality_plan","traceability"],"check_kind_groups":[],"waivable":false},{"id":"QUAL-HANDOFF-001","version":"1","statement":"Each delegation must include the scoped task, exact project-profile and rule versions, requirement and acceptance IDs, relevant design context, authorized actions, required evidence and return/stop conditions. Verify instruction discovery in the intended client; do not assume delegation propagates context.","source_ids":["SRC-CODEX-INSTRUCTIONS","SRC-COPILOT-INSTRUCTIONS"],"source_alignment":"Organization-owned handoff contract using public client-discovery guidance; supported instruction formats do not prove runtime loading or compliance.","responsibilities":["planner","implementer","reviewer","quality_checker","triage"],"phases":["planning","implementation","verification","review"],"verification":"manual","artifacts":["quality_plan","traceability"],"check_kind_groups":[],"waivable":false},{"id":"QUAL-SW-001","version":"1","statement":"For executable software, bind PR checks for build, lint, tests and static security analysis to the workflow contract. Select concrete project tools and scope; evaluate relevant integration and critical acceptance behavior in the test strategy.","source_ids":["SRC-ISO-25010","SRC-MICROSOFT-SDL"],"source_alignment":"Organization-owned requirement informed by the referenced public scopes; no normative clause conformance claimed.","responsibilities":["planner","implementer","quality_checker","reviewer"],"phases":["planning","verification"],"verification":"hybrid","artifacts":["test_strategy","traceability"],"check_kind_groups":[["build"],["lint"],["test"],["sast"]],"waivable":true},{"id":"QUAL-SEC-001","version":"1","statement":"Document material trust boundaries, threats and security assumptions. Verify relevant authorization, input handling, data protection and failure behavior with targeted security tests and analysis, and track unresolved security risk before release.","source_ids":["SRC-MICROSOFT-SDL"],"source_alignment":"Organization-owned selection informed by Microsoft public security practices; adoption does not claim compliance with Microsoft internal SDL requirements.","responsibilities":["planner","implementer","quality_checker","reviewer"],"phases":["design","implementation","verification","release"],"verification":"hybrid","artifacts":["quality_plan","traceability"],"check_kind_groups":[["sast"]],"waivable":true},{"id":"QUAL-PY-001","version":"1","statement":"For Python components, select supported runtime/tool versions and project coding rules. Bind PR lint and test commands; assess typing, dependency and packaging checks according to component risk and distribution model.","source_ids":["SRC-MICROSOFT-SDL"],"source_alignment":"Organization-owned Python refinement; specific style, type and packaging tools are selected by the project, not asserted as a normative SDL requirement.","responsibilities":["planner","implementer","quality_checker","reviewer"],"phases":["planning","implementation","verification"],"verification":"hybrid","artifacts":["test_strategy","traceability"],"check_kind_groups":[["lint"],["test"]],"waivable":true},{"id":"QUAL-TS-001","version":"1","statement":"For TypeScript components, select supported runtime/tool versions and project coding rules. Bind PR lint, typecheck and test commands; test runtime boundaries where static types cannot establish external-data validity.","source_ids":["SRC-MICROSOFT-SDL"],"source_alignment":"Organization-owned TypeScript refinement; concrete compiler, style and runtime checks are selected by the project.","responsibilities":["planner","implementer","quality_checker","reviewer"],"phases":["planning","implementation","verification"],"verification":"hybrid","artifacts":["test_strategy","traceability"],"check_kind_groups":[["lint"],["typecheck"],["test"]],"waivable":true},{"id":"QUAL-HIGH-001","version":"1","statement":"For high-risk changes, obtain independent design and behavior/security review and meaningful negative, compatibility and recovery coverage. Identify missing permissions, environments and manual approvals; unresolved mandatory evidence blocks completion.","source_ids":["SRC-MICROSOFT-SDL","SRC-ISO-12207"],"source_alignment":"Organization-owned requirement informed by the referenced public scopes; no normative clause conformance claimed.","responsibilities":["planner","implementer","quality_checker","reviewer"],"phases":["planning","design","verification","review"],"verification":"hybrid","artifacts":["quality_plan","test_strategy","traceability"],"check_kind_groups":[["test"]],"waivable":true},{"id":"QUAL-AGENT-001","version":"1","statement":"For agentic systems, test the complete task-to-dispatch-to-worker-to-review-to-gate-to-return chain, including scoped context, results, state transitions, rejection, cancellation and pause/resume where supported. Test invalid or missing evidence and authority boundaries; worker-only tests do not establish chain behavior.","source_ids":["SRC-CODEX-INSTRUCTIONS","SRC-COPILOT-INSTRUCTIONS"],"source_alignment":"Organization-owned agentic-system behavioral test requirement; client documentation informs discovery limits, not a claim that either provider implements this chain.","responsibilities":["planner","implementer","quality_checker","reviewer"],"phases":["design","implementation","verification"],"verification":"hybrid","artifacts":["test_strategy","traceability"],"check_kind_groups":[["test"]],"waivable":true},{"id":"QUAL-CPP-001","version":"1","statement":"Reference-only: before enabling C++17 quality rules, review the chosen compiler/toolchain and a C++17-compatible subset of the guide, define concrete checks and portability tests, and independently review profile activation.","source_ids":["SRC-GOOGLE-CPP"],"source_alignment":"Reference-only inactive rule. Google guidance currently targets C++20; no Google C++17 rules or compliance are adopted.","responsibilities":["planner","reviewer"],"phases":["planning"],"verification":"manual","artifacts":["quality_plan"],"check_kind_groups":[],"waivable":false},{"id":"QUAL-IEC-001","version":"1","statement":"Reference-only: before adopting a safety or medical software standard, review full authorized text, project applicability, edition-specific obligations, lifecycle evidence and any certification scheme with qualified human ownership through a separate scoped profile integration.","source_ids":["SRC-IEC-61508","SRC-IEC-62304"],"source_alignment":"Reference-only inactive rule. Public IEC product scope establishes relevance only, not clause adoption, safety integrity, medical compliance or certification.","responsibilities":["planner","reviewer"],"phases":["planning"],"verification":"manual","artifacts":["quality_plan"],"check_kind_groups":[],"waivable":false}],"profiles":[{"id":"agentic","version":"1","description":"Behavioral verification of supported agent delegation, review, gate, return and recovery chains.","enabled":true,"rules":["QUAL-AGENT-001"],"workflow_profiles":[]},{"id":"baseline","version":"1","description":"Shared requirements, design, implementation, testing, documentation, evidence, review and handoff duties.","enabled":true,"rules":["QUAL-REQ-001","QUAL-DES-001","QUAL-CODE-001","QUAL-TEST-001","QUAL-DOC-001","QUAL-EVID-001","QUAL-REVIEW-001","QUAL-HANDOFF-001"],"workflow_profiles":[]},{"id":"cpp17","version":"1","description":"Reference-only C++17 integration placeholder; compatible guide subset and compiler checks are not adopted.","enabled":false,"rules":["QUAL-CPP-001"],"workflow_profiles":[]},{"id":"high-risk","version":"1","description":"Additional independent review and negative/compatibility/recovery evidence for high-risk work.","enabled":true,"rules":["QUAL-HIGH-001"],"workflow_profiles":[]},{"id":"iec61508","version":"1","description":"Reference-only functional-safety placeholder; full-text obligations and applicability are not adopted.","enabled":false,"rules":["QUAL-IEC-001"],"workflow_profiles":[]},{"id":"iec62304","version":"1","description":"Reference-only medical-device software placeholder; full-text obligations and applicability are not adopted.","enabled":false,"rules":["QUAL-IEC-001"],"workflow_profiles":[]},{"id":"python","version":"1","description":"Python component checks; select alongside baseline and the applicable software/risk profiles.","enabled":true,"rules":["QUAL-PY-001"],"workflow_profiles":["python"]},{"id":"software","version":"1","description":"Executable software with build, lint, tests, security analysis and threat-informed review.","enabled":true,"rules":["QUAL-SW-001","QUAL-SEC-001"],"workflow_profiles":[]},{"id":"typescript","version":"1","description":"TypeScript component checks; select alongside baseline and the applicable software/risk profiles.","enabled":true,"rules":["QUAL-TS-001"],"workflow_profiles":["typescript"]}]}'
    missing = object()
    config_path = '.engineering-backbone/quality-profile.json'
    json_limit = 262144
    document_limit = 1048576
    identifier = re.compile(r'[A-Za-z][A-Za-z0-9_.-]{0,63}\Z')
    document_keys = {'quality_plan', 'test_strategy', 'traceability', 'exceptions'}
    workflow_profiles = {'docs', 'python', 'typescript', 'go', 'dotnet'}
    workflow_kinds = {'docs', 'build', 'lint', 'test', 'typecheck', 'browser', 'api',
                      'migration', 'sast', 'dependency', 'container', 'iac',
                      'release-integrity', 'provenance', 'signature', 'sbom',
                      'deployment-smoke', 'rollback', 'monitoring'}
    workflow_phases = {'pr', 'maintenance', 'release', 'deploy'}
    csv_headers = ('rule_id', 'requirement_id', 'risk', 'architecture', 'tests',
                   'check_ids', 'evidence', 'status')

    def fail(message):
        raise ValueError(message)

    def text(value, label, *, empty=False, limit=4096):
        if (not isinstance(value, str) or len(value) > limit
                or (not empty and not value.strip())
                or any(ord(char) < 32 or 127 <= ord(char) <= 159 for char in value)):
            fail('Invalid ' + label)
        try:
            value.encode('utf-8')
        except UnicodeError:
            fail('Invalid UTF-8 ' + label)
        return value

    def object_keys(value, expected, label):
        if not isinstance(value, dict) or set(value) != expected:
            fail(label + ' has missing or unknown keys')

    def ids(value, allowed, label, *, maximum=256):
        if (not isinstance(value, list) or len(value) > maximum
                or any(not isinstance(item, str) or item not in allowed for item in value)
                or len(value) != len(set(value))):
            fail('Invalid or duplicate ' + label)
        return set(value)

    def id_value(value, label):
        if not isinstance(value, str) or identifier.fullmatch(value) is None:
            fail('Invalid ' + label)
        return value

    def safe_path(value, *, directory=False, absent=False):
        value = Path(value)
        if '..' in value.parts:
            fail('Parent traversal in filesystem path')
        value = Path(os.path.abspath(value))
        current = Path(value.anchor)
        for part in value.parts[1:]:
            current = current / part
            try:
                mode = current.lstat().st_mode
            except FileNotFoundError:
                if absent:
                    return value
                fail('Required filesystem path is absent')
            if stat.S_ISLNK(mode):
                fail('Symlink in filesystem path')
            if current != value and not stat.S_ISDIR(mode):
                fail('Non-directory filesystem ancestor')
        mode = value.stat().st_mode
        if directory and not stat.S_ISDIR(mode):
            fail('Input root is not a directory')
        if not directory and not stat.S_ISREG(mode):
            fail('Input is not a regular file')
        return value

    def relative_path(value, label, *, empty=False):
        value = text(value, label, empty=empty, limit=512)
        if empty and value == '':
            return value
        if (value.startswith('/') or '\\' in value or ':' in value
                or any(part in ('', '.', '..') for part in value.split('/'))):
            fail(label + ' must be a safe relative file path')
        return value

    def read_bytes(value, *, limit, absent=False):
        path = safe_path(value, absent=absent)
        if absent and not path.exists():
            return missing
        if path.stat().st_size > limit:
            fail('Input exceeds size limit')
        with path.open('rb') as handle:
            result = handle.read(limit + 1)
        if len(result) > limit:
            fail('Input exceeds size limit')
        return result

    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                fail('Duplicate JSON object key')
            result[key] = value
        return result

    def read_json(value, *, absent=False):
        data = read_bytes(value, limit=json_limit, absent=absent)
        if data is missing:
            return missing
        return json.loads(data.decode('utf-8'), object_pairs_hook=pairs,
                          parse_constant=lambda value: fail('Invalid JSON number'))

    def read_document(folder, value, *, required=False):
        if not value:
            if required:
                fail('Required quality document path is empty')
            return None
        data = read_bytes(folder / value, limit=document_limit)
        document = data.decode('utf-8')
        if '\x00' in document:
            fail('Quality document contains a NUL character')
        if required and not document.strip():
            fail('Required quality document is empty')
        return document

    def read_evidence(folder, value):
        # Evidence may be a text report, screenshot or PDF. Read bounded regular
        # bytes without interpreting the contents or authenticating the claim.
        if not read_bytes(folder / value, limit=document_limit):
            fail('Required evidence file is empty')

    def catalog():
        value = json.loads(catalog_json, object_pairs_hook=pairs,
                           parse_constant=lambda value: fail('Invalid trusted JSON number'))
        object_keys(value, {'version', 'sources', 'rules', 'profiles'}, 'Trusted catalog')
        if value['version'] != '1.0.0':
            fail('Unsupported trusted catalog version')
        for key in ('sources', 'rules', 'profiles'):
            if not isinstance(value[key], list) or not 1 <= len(value[key]) <= 256:
                fail('Invalid trusted catalog ' + key)
        sources = {}
        for entry in value['sources']:
            object_keys(entry, {'id', 'title', 'edition', 'url', 'status', 'access',
                               'adoption', 'verified_sections'}, 'Catalog source')
            key = id_value(entry['id'], 'source ID')
            if key in sources:
                fail('Duplicate source ID')
            for name in ('title', 'edition', 'url', 'status', 'access', 'adoption'):
                text(entry[name], 'source ' + name)
            if not isinstance(entry['verified_sections'], list) or len(entry['verified_sections']) > 100:
                fail('Invalid source verified sections')
            for section in entry['verified_sections']:
                text(section, 'source verified section')
            sources[key] = entry
        rules = {}
        for entry in value['rules']:
            object_keys(entry, {'id', 'version', 'statement', 'source_ids',
                               'source_alignment', 'responsibilities', 'phases',
                               'verification', 'artifacts', 'check_kind_groups',
                               'waivable'}, 'Catalog rule')
            key = id_value(entry['id'], 'rule ID')
            if key in rules or entry['version'] != '1':
                fail('Duplicate rule ID or unsupported rule version')
            text(entry['statement'], 'rule statement')
            text(entry['source_alignment'], 'rule source alignment')
            if not ids(entry['source_ids'], sources, 'rule sources'):
                fail('Rule has no source')
            if not ids(entry['responsibilities'], {'planner', 'implementer', 'reviewer',
                       'quality_checker', 'triage'}, 'rule responsibilities', maximum=5):
                fail('Rule has no responsibility')
            if not ids(entry['phases'], {'planning', 'design', 'implementation',
                       'verification', 'review', 'publication', 'release', 'operation'},
                       'rule phases', maximum=8):
                fail('Rule has no phase')
            if (not isinstance(entry['verification'], str)
                    or entry['verification'] not in {'automatic', 'manual', 'hybrid'}):
                fail('Invalid rule verification')
            ids(entry['artifacts'], document_keys - {'exceptions'}, 'rule artifacts', maximum=3)
            if type(entry['waivable']) is not bool:
                fail('Invalid rule waiver flag')
            groups = entry['check_kind_groups']
            if not isinstance(groups, list) or len(groups) > len(workflow_kinds):
                fail('Invalid rule check-kind groups')
            for group in groups:
                if not ids(group, workflow_kinds, 'rule check kinds', maximum=len(workflow_kinds)):
                    fail('Empty rule check-kind group')
            rules[key] = entry
        profiles = {}
        for entry in value['profiles']:
            object_keys(entry, {'id', 'version', 'description', 'enabled', 'rules',
                               'workflow_profiles'}, 'Catalog profile')
            key = id_value(entry['id'], 'catalog profile ID')
            if key in profiles or entry['version'] != '1' or type(entry['enabled']) is not bool:
                fail('Duplicate profile ID or invalid catalog profile version/flag')
            text(entry['description'], 'catalog profile description')
            if not ids(entry['rules'], rules, 'catalog profile rules'):
                fail('Catalog profile has no rules')
            ids(entry['workflow_profiles'], workflow_profiles, 'catalog workflow profiles', maximum=5)
            profiles[key] = entry
        if 'baseline' not in profiles or not profiles['baseline']['enabled']:
            fail('Trusted catalog lacks the enabled baseline profile')
        if any(rules[key]['waivable'] for key in profiles['baseline']['rules']):
            fail('Baseline rules cannot be waived')
        return value, rules, profiles

    def package(folder, authority, *, central=False):
        prefix = folder / ('standards' if central else '.engineering-backbone/standards')
        for key in ('sources', 'rules'):
            expected = {'schema_version': '1', 'version': authority['version'],
                        key: authority[key]}
            if read_json(prefix / (key + '.json')) != expected:
                fail('Managed ' + key + ' catalog differs from trusted authority')
        profile_dir = safe_path(prefix / 'profiles', directory=True)
        expected_names = {entry['id'] + '.json' for entry in authority['profiles']}
        actual_names = set()
        for path in profile_dir.iterdir():
            if len(actual_names) >= 256:
                fail('Managed catalog exceeds profile-file limit')
            actual_names.add(path.name)
        if actual_names != expected_names:
            fail('Managed catalog profile files differ from trusted authority')
        for entry in authority['profiles']:
            if read_json(profile_dir / (entry['id'] + '.json')) != entry:
                fail('Managed profile catalog differs from trusted authority')

    def workflow(folder, *, needed=False):
        value = read_json(folder / '.engineering-backbone/workflows.json', absent=True)
        if value is missing:
            if needed:
                fail('Quality bindings require an active complete workflow kit')
            return None
        object_keys(value, {'schema_version', 'enabled', 'profiles', 'capabilities',
                           'runtimes', 'checks'}, 'Workflow configuration')
        if value['schema_version'] != '1' or type(value['enabled']) is not bool:
            fail('Invalid workflow configuration version/flag')
        selected = ids(value['profiles'], workflow_profiles, 'workflow profiles', maximum=5)
        capabilities = ids(value['capabilities'], {'dependencies', 'web', 'api', 'database',
                          'container', 'iac', 'release', 'deploy'}, 'workflow capabilities', maximum=8)
        runtime_for = {'python': 'python', 'typescript': 'node', 'go': 'go', 'dotnet': 'dotnet'}
        runtimes = value['runtimes']
        if not isinstance(runtimes, dict) or set(runtimes) - set(runtime_for.values()):
            fail('Invalid workflow runtimes')
        for name, version in runtimes.items():
            text(version, 'workflow runtime version', limit=32)
            pattern = r'[0-9]{1,3}(?:\.[0-9]{1,3}){0,2}' + (r'(?:\.x)?' if name == 'dotnet' else '')
            if re.fullmatch(pattern, version) is None:
                fail('Invalid workflow runtime version')
        checks = value['checks']
        if not isinstance(checks, list) or len(checks) > 100:
            fail('Invalid workflow checks')
        check_map, coverage = {}, set()
        release_kinds = {'release-integrity', 'provenance', 'signature', 'sbom'}
        deploy_kinds = {'deployment-smoke', 'rollback', 'monitoring'}
        for check in checks:
            object_keys(check, {'id', 'kind', 'argv', 'cwd', 'timeout_seconds', 'phases'}, 'Workflow check')
            key = id_value(check['id'], 'workflow check ID')
            if key in check_map:
                fail('Duplicate workflow check ID')
            if not isinstance(check['kind'], str) or check['kind'] not in workflow_kinds:
                fail('Invalid workflow check kind')
            if not isinstance(check['argv'], list) or not 1 <= len(check['argv']) <= 64:
                fail('Invalid workflow command arguments')
            for argument in check['argv']:
                text(argument, 'workflow command argument', empty=True)
            if not check['argv'][0].strip():
                fail('Workflow command executable is empty')
            if check['cwd'] != '.':
                relative_path(check['cwd'], 'Workflow working directory')
            if type(check['timeout_seconds']) is not int or not 1 <= check['timeout_seconds'] <= 1800:
                fail('Invalid workflow check timeout')
            phases = ids(check['phases'], workflow_phases, 'workflow check phases', maximum=4)
            allowed = ({'release'} if check['kind'] in release_kinds else
                       {'deploy'} if check['kind'] in deploy_kinds else
                       {'pr', 'maintenance'} if check['kind'] in {'dependency', 'container'} else {'pr'})
            if not phases or phases - allowed:
                fail('Workflow kind does not support selected phases')
            coverage.update((check['kind'], phase) for phase in phases)
            check_map[key] = check
        if value['enabled'] or needed:
            if not value['enabled'] or not selected:
                fail('Quality bindings require an active complete workflow kit')
            if any(runtime_for[key] not in runtimes for key in selected if key in runtime_for):
                fail('Required workflow runtime is missing')
            required = set()
            for key in selected:
                required.update((kind, 'pr') for kind in
                                (['docs'] if key == 'docs' else ['build', 'lint', 'test', 'sast']))
                if key == 'typescript':
                    required.add(('typecheck', 'pr'))
            for capability, kind in [('web', 'browser'), ('api', 'api'),
                                      ('database', 'migration'), ('iac', 'iac')]:
                if capability in capabilities:
                    required.add((kind, 'pr'))
            for capability, kind in (('dependencies', 'dependency'), ('container', 'container')):
                if capability in capabilities:
                    required.update((kind, phase) for phase in ('pr', 'maintenance'))
            if 'release' in capabilities:
                required.update((kind, 'release') for kind in ('release-integrity', 'provenance', 'signature'))
                if capabilities & {'dependencies', 'container'}:
                    required.add(('sbom', 'release'))
            if 'deploy' in capabilities:
                required.update((kind, 'deploy') for kind in deploy_kinds)
            if required - coverage:
                fail('Required workflow checks are missing')
        return value

    def profile(folder, rules, profiles, authority, *, approved=False):
        value = read_json(folder / config_path, absent=True)
        if value is missing:
            return None
        object_keys(value, {'schema_version', 'enabled', 'catalog_version', 'backbone_ref',
                           'profiles', 'documents', 'checks', 'exceptions'}, 'Quality profile')
        if value['schema_version'] != '1' or type(value['enabled']) is not bool:
            fail('Invalid quality profile version/flag')
        if value['catalog_version'] != authority['version']:
            fail('Quality catalog version is not trusted')
        reference = text(value['backbone_ref'], 'backbone reference', empty=True, limit=40)
        if reference and re.fullmatch(r'[0-9a-fA-F]{40}', reference) is None:
            fail('Backbone reference must be a full commit SHA')
        selected = ids(value['profiles'], profiles, 'quality profiles')
        if any(not profiles[key]['enabled'] for key in selected):
            fail('Reference-only catalog profile cannot be selected')
        object_keys(value['documents'], document_keys, 'Quality document mapping')
        for key, path in value['documents'].items():
            relative_path(path, 'Quality document ' + key, empty=True)
        applicable = {key for profile_id in selected for key in profiles[profile_id]['rules']}
        bindings = value['checks']
        if not isinstance(bindings, list) or len(bindings) > 256:
            fail('Invalid quality check bindings')
        bound_rules = set()
        for binding in bindings:
            object_keys(binding, {'rule_id', 'check_ids'}, 'Quality check binding')
            rule_id = id_value(binding['rule_id'], 'bound rule ID')
            if rule_id not in applicable or rule_id in bound_rules:
                fail('Unknown, unselected or duplicate bound rule')
            check_ids = binding['check_ids']
            if (not isinstance(check_ids, list) or not 1 <= len(check_ids) <= 100
                    or any(not isinstance(key, str) or identifier.fullmatch(key) is None for key in check_ids)
                    or len(check_ids) != len(set(check_ids))):
                fail('Invalid or duplicate bound check IDs')
            bound_rules.add(rule_id)
        exceptions = value['exceptions']
        if not isinstance(exceptions, list) or len(exceptions) > 256:
            fail('Invalid quality exceptions')
        exception_ids = set()
        for exception in exceptions:
            object_keys(exception, {'rule_id', 'scope', 'reason', 'owner', 'approved_by',
                                   'expires_on', 'compensating_check_ids', 'evidence_path'}, 'Quality exception')
            rule_id = id_value(exception['rule_id'], 'exception rule ID')
            if rule_id not in applicable or rule_id in exception_ids or not rules[rule_id]['waivable']:
                fail('Unknown, unselected, duplicate or disallowed exception rule')
            exception_ids.add(rule_id)
            for key in ('scope', 'reason', 'owner', 'approved_by'):
                text(exception[key], 'exception ' + key)
            expiry = text(exception['expires_on'], 'exception expiry', limit=10)
            if (re.fullmatch(r'\d{4}-\d{2}-\d{2}', expiry) is None
                    or not approved and date.fromisoformat(expiry) < date.today()):
                fail('Invalid or expired quality exception')
            date.fromisoformat(expiry)
            compensating = exception['compensating_check_ids']
            if (not isinstance(compensating, list) or not 1 <= len(compensating) <= 100
                    or any(not isinstance(key, str) or identifier.fullmatch(key) is None for key in compensating)
                    or len(compensating) != len(set(compensating))):
                fail('Invalid compensating check IDs')
            evidence = relative_path(exception['evidence_path'], 'Exception evidence path')
            read_evidence(folder, evidence)
        package(folder, authority, central=source)
        return value

    def delimited(value, label):
        if not value:
            return []
        values = value.split(';')
        if any(not entry or entry != entry.strip() for entry in values) or len(values) != len(set(values)):
            fail('Invalid or duplicate CSV ' + label)
        return values

    def validate_content(folder, value, rules, profiles, *, complete=False, approved_workflow=None):
        if value is None:
            return
        complete = complete or value['enabled']
        selected = set(value['profiles'])
        applicable = {key for profile_id in selected for key in profiles[profile_id]['rules']}
        if complete and ('baseline' not in selected or not value['backbone_ref']):
            fail('Complete quality profile requires baseline and a full backbone reference')
        needed_workflow = complete or bool(value['checks']) or bool(value['exceptions'])
        current_workflow = workflow(folder, needed=needed_workflow)
        effective_workflow = current_workflow
        if current_workflow is not None and approved_workflow is not None:
            effective_workflow = dict(current_workflow)
            approved_checks = {check['id']: check for check in approved_workflow['checks']}
            effective_workflow['checks'] = [approved_checks.get(check['id'], check)
                                            for check in current_workflow['checks']]
            # Existing workflow profile selections cannot disappear here either.
            if set(approved_workflow['profiles']) - set(current_workflow['profiles']):
                fail('Approved workflow profiles cannot be removed')
        check_map = ({check['id']: check for check in effective_workflow['checks']}
                     if effective_workflow is not None else {})
        pr_checks = {key: check for key, check in check_map.items() if 'pr' in check['phases']}
        for profile_id in selected:
            required = set(profiles[profile_id]['workflow_profiles'])
            if complete and (effective_workflow is None or required - set(effective_workflow['profiles'])):
                fail('Required quality language workflow profile is missing')
        binding_map = {entry['rule_id']: set(entry['check_ids']) for entry in value['checks']}
        exceptions = {entry['rule_id']: entry for entry in value['exceptions']}
        for rule_id, bound in binding_map.items():
            if bound - set(pr_checks):
                fail('Quality binding references an unknown or non-PR workflow check')
        for exception in value['exceptions']:
            if set(exception['compensating_check_ids']) - set(pr_checks):
                fail('Exception references an unknown or non-PR workflow check')
        for rule_id in applicable:
            rule = rules[rule_id]
            if complete:
                for artifact in rule['artifacts']:
                    if not value['documents'][artifact]:
                        fail('Required rule artifact path is missing')
                if rule_id not in exceptions:
                    covered = {pr_checks[key]['kind'] for key in binding_map.get(rule_id, set())}
                    if any(not covered.intersection(group) for group in rule['check_kind_groups']):
                        fail('Required rule PR check-kind coverage is missing: ' + rule_id)
        documents = {}
        for key, path in value['documents'].items():
            required = complete and key != 'exceptions' or key == 'exceptions' and bool(exceptions)
            documents[key] = read_document(folder, path, required=required)
        trace = documents['traceability']
        if trace is None:
            return
        reader = csv.DictReader(io.StringIO(trace, newline=''), strict=True)
        if tuple(reader.fieldnames or ()) != csv_headers:
            fail('Traceability CSV has missing, reordered or unknown columns')
        mapped, trace_checks = set(), {}
        for index, row in enumerate(reader):
            if index >= 4096 or set(row) != set(csv_headers) or any(value is None for value in row.values()):
                fail('Traceability CSV is malformed or exceeds row limit')
            for key, cell in row.items():
                text(cell, 'CSV ' + key, empty=True, limit=65536)
            rule_id = row['rule_id']
            if rule_id not in applicable:
                fail('Traceability CSV references an unknown or unselected rule')
            if row['status'] not in {'pending', 'planned', 'verified', 'gap'}:
                fail('Invalid traceability declaration status')
            if complete and any(not row[key].strip() for key in ('requirement_id', 'risk', 'architecture', 'tests')):
                fail('Complete traceability row lacks requirement/risk/design/test mapping')
            row_checks = set(delimited(row['check_ids'], 'check IDs'))
            allowed = binding_map.get(rule_id, set()) | set(exceptions.get(rule_id, {}).get('compensating_check_ids', []))
            if row_checks - set(pr_checks) or row_checks - allowed:
                fail('Traceability check IDs are unknown, non-PR or not bound to their rule')
            evidence = delimited(row['evidence'], 'evidence paths')
            if row['status'] == 'verified' and not evidence:
                fail('Verified declaration lacks a regular evidence file')
            for reference in evidence:
                relative_path(reference, 'Traceability evidence path')
                safe_path(folder / reference, absent=row['status'] != 'verified')
                if row['status'] == 'verified':
                    read_evidence(folder, reference)
            mapped.add(rule_id)
            trace_checks.setdefault(rule_id, set()).update(row_checks)
        if complete:
            if applicable - mapped:
                fail('Traceability CSV does not map every selected rule')
            for rule_id, bound in binding_map.items():
                if bound - trace_checks.get(rule_id, set()):
                    fail('Traceability CSV omits declared rule check bindings')

    try:
        root = safe_path(root, directory=True)
        authority, rules, profiles = catalog()
        if source:
            package(root, authority, central=True)
        candidate = profile(root, rules, profiles, authority)
        base = None
        base_workflow = None
        if trusted_base is not None:
            trusted_base = safe_path(trusted_base, directory=True)
            base = profile(trusted_base, rules, profiles, authority, approved=True)
            validate_content(trusted_base, base, rules, profiles)
            if base is not None and base['enabled']:
                base_workflow = workflow(trusted_base, needed=True)
                if candidate is None or not candidate['enabled']:
                    fail('Active quality profile cannot be removed or disabled')
                if set(base['profiles']) - set(candidate['profiles']):
                    fail('Approved quality profiles cannot be removed')
                candidate_bindings = {item['rule_id']: set(item['check_ids']) for item in candidate['checks']}
                for binding in base['checks']:
                    if set(binding['check_ids']) - candidate_bindings.get(binding['rule_id'], set()):
                        fail('Approved rule check bindings cannot be removed')
                old_exceptions = {item['rule_id']: item for item in base['exceptions']}
                for exception in candidate['exceptions']:
                    if old_exceptions.get(exception['rule_id']) != exception:
                        fail('Active profile cannot introduce or alter an approved exception')
            if candidate is not None and candidate['enabled'] and (base is None or not base['enabled']):
                if base is None:
                    fail('Quality activation requires an already reviewed inactive seed')
                validate_content(trusted_base, base, rules, profiles, complete=True)
                if candidate != dict(base, enabled=True):
                    fail('Quality activation must match the reviewed seed except enabled')
        validate_content(root, candidate, rules, profiles, approved_workflow=base_workflow)
        return []
    except (ValueError, OSError, UnicodeError, csv.Error, RecursionError) as exc:
        return ['Quality framework: ' + str(exc)]


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest='command', required=True)
    validate = subcommands.add_parser('validate')
    validate.add_argument('--root', default='.')
    validate.add_argument('--trusted-base')
    validate.add_argument('--source', action='store_true')
    args = parser.parse_args(argv)
    errors = quality_errors(args.root, args.trusted_base, source=args.source)
    for error in errors:
        print(error)
    if errors:
        return 1
    print('PASS: structural quality contracts only; not semantic approval or certification')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
