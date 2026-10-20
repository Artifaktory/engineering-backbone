#!/usr/bin/env python3
"""Pinned, credential-free native discovery smoke; not model qualification."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import dataclass
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import platform
import shutil
import signal
import stat
import subprocess
import tarfile
import tempfile
import threading
import time
import urllib.request
import zipfile


VERSION = '1.19.0'
SOURCE_COMMIT = '733b2c627e5aec39cb33cc22373bdce33053ef2c'
RELEASES = {
    'Linux': ('opencode-linux-x64.tar.gz',
              '7bb9e61ad6feacf2e89c10a6a2c1840e3de4220bb50ba1fc7110f31806076aec',
              'opencode'),
    'Windows': ('opencode-windows-x64.zip',
                '17108e9448c4fdad48eb8714c4ed6f5dfc9cf86c2eb8f2ce5d02043fef806eb5',
                'opencode.exe'),
}
ROLES = ('planner', 'implementer', 'reviewer', 'quality-checker', 'triage')
SKILLS = ('task-intake', 'implementation-plan', 'bug-reproduction',
          'test-and-quality', 'code-review', 'finding-triage', 'delta-review',
          'docs-traceability')
MAX_ARCHIVE = 512 * 1024 * 1024
MAX_OUTPUT = 2 * 1024 * 1024
MAX_REQUEST = 2 * 1024 * 1024
MAX_REQUESTS = 30
CALL_ID = 'call_backbone_smoke_write'
ROLE_MARKER = 'BACKBONE_NATIVE_SMOKE_SELECTED_REVIEWER'
NESTED_MARKER = 'BACKBONE_NATIVE_SMOKE_NESTED_INSTRUCTIONS'


class SmokeError(RuntimeError):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_digest(path: Path, limit: int = MAX_ARCHIVE) -> str:
    if path.stat().st_size > limit:
        raise SmokeError('file exceeds size bound')
    result = hashlib.sha256()
    with path.open('rb') as stream:
        while chunk := stream.read(1024 * 1024):
            result.update(chunk)
    return result.hexdigest()


def download(url: str, target: Path) -> None:
    started = time.monotonic()
    total = 0
    with urllib.request.urlopen(url, timeout=30) as response, target.open('wb') as out:
        while chunk := response.read(1024 * 1024):
            total += len(chunk)
            if total > MAX_ARCHIVE or time.monotonic() - started > 180:
                raise SmokeError('archive download exceeded size/time bound')
            out.write(chunk)


def extract_verified(archive: Path, target: Path, expected: str, binary_name: str) -> Path:
    """Verify first, then extract only one regular root executable (no extractall)."""
    if file_digest(archive) != expected:
        raise SmokeError('archive SHA-256 mismatch; executable was not extracted')
    binary = target / binary_name
    target.mkdir(parents=True, exist_ok=True)
    if archive.name.endswith('.zip'):
        with zipfile.ZipFile(archive) as bundle:
            members = bundle.infolist()
            if len(members) != 1 or members[0].filename != binary_name:
                raise SmokeError('archive must contain exactly the root executable')
            item = members[0]
            mode = item.external_attr >> 16
            if item.is_dir() or stat.S_ISLNK(mode) or (stat.S_IFMT(mode) not in (0, stat.S_IFREG)):
                raise SmokeError('archive executable must be a regular file')
            if not 0 < item.file_size <= MAX_ARCHIVE:
                raise SmokeError('archive executable exceeds size bound')
            with bundle.open(item) as source, binary.open('wb') as out:
                shutil.copyfileobj(source, out, 1024 * 1024)
    else:
        with tarfile.open(archive, 'r:gz') as bundle:
            item = bundle.next()
            if item is None or item.name != binary_name or not item.isfile():
                raise SmokeError('archive must contain exactly the regular root executable')
            if not 0 < item.size <= MAX_ARCHIVE:
                raise SmokeError('archive executable exceeds size bound')
            source = bundle.extractfile(item)
            if source is None:
                raise SmokeError('archive executable cannot be read')
            with source, binary.open('wb') as out:
                shutil.copyfileobj(source, out, 1024 * 1024)
            if bundle.next() is not None:
                binary.unlink()
                raise SmokeError('archive must contain exactly the root executable')
    binary.chmod(0o700)
    return binary


def isolated_environment(root: Path, inherited: dict[str, str] | None = None) -> dict[str, str]:
    # Explicit OS necessities only. In particular no tokens, OPENCODE_*, GIT_*,
    # NODE_OPTIONS, provider credentials, user config or inherited proxy values.
    inherited = os.environ if inherited is None else inherited
    allowed = {'PATH', 'SYSTEMROOT', 'WINDIR', 'COMSPEC', 'PATHEXT'}
    env = {key: value for key, value in inherited.items() if key.upper() in allowed}
    directories = {
        'HOME': root / 'home', 'USERPROFILE': root / 'home',
        'XDG_CONFIG_HOME': root / 'config', 'XDG_DATA_HOME': root / 'data',
        'XDG_STATE_HOME': root / 'state', 'XDG_CACHE_HOME': root / 'cache',
        'APPDATA': root / 'appdata', 'LOCALAPPDATA': root / 'localappdata',
        'TEMP': root / 'tmp', 'TMP': root / 'tmp', 'TMPDIR': root / 'tmp',
    }
    for name, directory in directories.items():
        directory.mkdir(parents=True, exist_ok=True)
        env[name] = str(directory)
    env.update({
        'OPENCODE_PURE': '1', 'OPENCODE_DISABLE_AUTOUPDATE': '1',
        'OPENCODE_DISABLE_MODELS_FETCH': '1', 'OPENCODE_DISABLE_AUTOCOMPACT': '1',
        'OPENCODE_DISABLE_TERMINAL_TITLE': '1', 'OPENCODE_DISABLE_FFF': '1',
        'OPENCODE_EXPERIMENTAL_DISABLE_FILEWATCHER': 'true',
        'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull,
        'NO_COLOR': '1', 'CI': '1',
        # These are convenience restrictions, not a network sandbox claim.
        'HTTP_PROXY': 'http://127.0.0.1:9', 'HTTPS_PROXY': 'http://127.0.0.1:9',
        'NO_PROXY': '127.0.0.1,localhost',
        'npm_config_registry': 'http://127.0.0.1:9',
    })
    return env


@dataclass
class CommandResult:
    code: int
    stdout: str
    stderr: str


def stop_process(process: subprocess.Popen) -> None:
    if os.name == 'nt':
        # Terminate the process tree as well as the main process on timeout.
        taskkill = Path(os.environ.get('SystemRoot', r'C:\Windows')) / 'System32/taskkill.exe'
        try:
            subprocess.run([str(taskkill), '/PID', str(process.pid), '/T', '/F'],
                           capture_output=True, timeout=10, check=False)
        except (OSError, subprocess.TimeoutExpired):
            pass
        if process.poll() is None:
            process.kill()
    else:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    process.wait(timeout=10)


def run_command(argv: list[str], cwd: Path, env: dict[str, str], report: dict,
                timeout: float = 60) -> CommandResult:
    started = time.monotonic()
    failure = None
    with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        process = subprocess.Popen(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                                   stdout=stdout, stderr=stderr,
                                   start_new_session=os.name != 'nt',
                                   creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0)
        while process.poll() is None:
            if time.monotonic() - started > timeout:
                failure = 'command timeout'
            elif os.fstat(stdout.fileno()).st_size + os.fstat(stderr.fileno()).st_size > MAX_OUTPUT:
                failure = 'command output limit'
            if failure:
                stop_process(process)
                break
            time.sleep(0.05)
        stdout.seek(0)
        stderr.seek(0)
        out, err = stdout.read(MAX_OUTPUT + 1), stderr.read(MAX_OUTPUT + 1)
        if len(out) + len(err) > MAX_OUTPUT:
            failure = 'command output limit'
    record = {
        'argv': argv, 'cwd': str(cwd), 'exit_code': process.returncode,
        'seconds': round(time.monotonic() - started, 3),
        'stdout_sha256': digest(out), 'stderr_sha256': digest(err),
        'stdout_bytes': len(out), 'stderr_bytes': len(err),
    }
    if failure:
        record['failure'] = failure
    report.setdefault('commands', []).append(record)
    if failure:
        raise SmokeError(failure)
    return CommandResult(process.returncode, out.decode('utf-8', errors='replace'),
                         err.decode('utf-8', errors='replace'))


def successful(result: CommandResult) -> str:
    if result.code != 0:
        # Isolated smoke output contains no host credentials; keep errors bounded.
        raise SmokeError(f'command exited {result.code}: {result.stderr[-2000:]}')
    return result.stdout


def message_text(payload: dict) -> str:
    return '\n'.join(message.get('content', '') if isinstance(message.get('content'), str)
                     else json.dumps(message.get('content', ''), ensure_ascii=False)
                     for message in payload.get('messages', []))


class CannedProvider:
    """A localhost-only canned protocol peer, without a real model or credentials."""
    def __init__(self, target: Path):
        self.target = target
        self.requests: list[dict] = []
        self.errors: list[str] = []
        self.lock = threading.Lock()

    def chunks(self, payload: dict) -> list[dict]:
        text = message_text(payload)
        tool_reply = any(item.get('role') == 'tool' and item.get('tool_call_id') == CALL_ID
                         for item in payload.get('messages', []))
        boundary = 'SMOKE_TOOL_BOUNDARY' in text and ROLE_MARKER in text
        delta = {'role': 'assistant', 'content': 'Native smoke complete.'}
        finish = 'stop'
        if boundary and not tool_reply:
            delta = {'role': 'assistant', 'tool_calls': [{
                'index': 0, 'id': CALL_ID, 'type': 'function',
                'function': {'name': 'write', 'arguments': json.dumps({
                    'filePath': str(self.target), 'content': 'This write must be refused.\n'})},
            }]}
            finish = 'tool_calls'
        base = {'id': 'chatcmpl-backbone-smoke', 'object': 'chat.completion.chunk',
                'created': 0, 'model': 'smoke'}
        return [dict(base, choices=[{'index': 0, 'delta': delta, 'finish_reason': None}]),
                dict(base, choices=[{'index': 0, 'delta': {}, 'finish_reason': finish}],
                     usage={'prompt_tokens': 1, 'completion_tokens': 1, 'total_tokens': 2})]

    @contextmanager
    def serve(self):
        owner = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_args):
                pass

            def do_POST(self):
                try:
                    self.connection.settimeout(5)
                    length = int(self.headers.get('Content-Length', '0'))
                    if self.path != '/v1/chat/completions' or not 0 < length <= MAX_REQUEST:
                        self.send_error(400)
                        return
                    payload = json.loads(self.rfile.read(length))
                    if not isinstance(payload, dict) or not isinstance(payload.get('messages'), list):
                        self.send_error(400)
                        return
                    with owner.lock:
                        if len(owner.requests) >= MAX_REQUESTS:
                            self.send_error(429)
                            return
                        owner.requests.append(payload)
                    chunks = owner.chunks(payload)
                    if payload.get('stream'):
                        body = ''.join('data: ' + json.dumps(chunk) + '\n\n' for chunk in chunks)
                        body += 'data: [DONE]\n\n'
                        content_type = 'text/event-stream'
                    else:
                        message = chunks[0]['choices'][0]['delta']
                        body = json.dumps({'id': 'chatcmpl-backbone-smoke',
                                           'object': 'chat.completion', 'created': 0,
                                           'model': 'smoke', 'choices': [{'index': 0,
                                           'message': message, 'finish_reason': chunks[1]['choices'][0]['finish_reason']}]})
                        content_type = 'application/json'
                    data = body.encode('utf-8')
                    self.send_response(200)
                    self.send_header('Content-Type', content_type)
                    self.send_header('Content-Length', str(len(data)))
                    self.end_headers()
                    self.wfile.write(data)
                except (ValueError, OSError) as error:
                    owner.errors.append(type(error).__name__)

        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        server.daemon_threads = True
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield f'http://127.0.0.1:{server.server_port}/v1'
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


def prepare_fixture(repo: Path, workspace: Path, report: dict) -> dict[str, str]:
    """Copy declared data only; do not copy candidate plugins, hooks or config layers."""
    config = json.loads((repo / 'opencode.json').read_text(encoding='utf-8'))
    if not isinstance(config, dict) or set(config) != {'$schema', 'instructions', 'permission'}:
        raise SmokeError('source native config is outside the smoke contract')
    instructions = config.get('instructions')
    if (not isinstance(instructions, list) or not instructions
            or any(not isinstance(item, str) for item in instructions)):
        raise SmokeError('source native instructions must be a nonempty list')
    names = ['opencode.json', *instructions,
             *[f'.opencode/agents/backbone-{role}.md' for role in ROLES],
             *[f'.opencode/skills/{skill}/SKILL.md' for skill in SKILLS]]
    expected = {}
    report['inputs'] = {}
    for name in dict.fromkeys(names):
        if not isinstance(name, str) or '\\' in name or ':' in name or name.startswith('/'):
            raise SmokeError('invalid source input path')
        parts = name.split('/')
        if any(part in ('', '.', '..') for part in parts):
            raise SmokeError('invalid source input path')
        source = repo
        for part in parts:
            source = source / part
            if source.is_symlink():
                raise SmokeError('symlinked source input')
        if not source.is_file() or source.stat().st_size > MAX_REQUEST:
            raise SmokeError(f'missing/oversized source input: {name}')
        original = source.read_bytes()
        text = original.decode('utf-8')
        if name in instructions and name.endswith('.md'):
            text += '\n\nBACKBONE_NATIVE_SMOKE_INSTRUCTION_' + digest(name.encode())[:16] + '\n'
        if name == '.opencode/agents/backbone-reviewer.md':
            text += '\n\n' + ROLE_MARKER + '\n'
        destination = workspace / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding='utf-8', newline='\n')
        report['inputs'][name] = {'source_sha256': digest(original),
                                  'fixture_sha256': digest(text.encode('utf-8'))}
        if name in instructions:
            expected[name] = text.strip()
    nested = workspace / 'nested'
    nested.mkdir()
    (nested / 'AGENTS.md').write_text(NESTED_MARKER + '\n', encoding='utf-8')
    return expected


def check_loaded(requests: list[dict], expected: dict[str, str], *, nested: bool) -> dict:
    candidates = [request for request in requests if ROLE_MARKER in message_text(request)]
    if not candidates:
        raise SmokeError('selected reviewer prompt absent from provider-received messages')
    # Every required instruction must coexist in the actual selected-agent request.
    for request in candidates:
        text = message_text(request)
        if all(content in text for content in expected.values()) and (not nested or NESTED_MARKER in text):
            return {'instruction_paths': list(expected), 'selected_role_marker': True,
                    'nested_marker': NESTED_MARKER in text,
                    'request_sha256': digest(json.dumps(request, sort_keys=True).encode())}
    raise SmokeError('required instruction bytes absent from selected-agent provider request')


def check_denial(requests: list[dict], target: Path, original: bytes) -> dict:
    initial = [request for request in requests if ROLE_MARKER in message_text(request)
               and 'SMOKE_TOOL_BOUNDARY' in message_text(request)
               and not any(item.get('tool_call_id') == CALL_ID for item in request.get('messages', []))]
    if not initial:
        raise SmokeError('tool-boundary request was not observed')
    advertised = {tool.get('function', {}).get('name') for request in initial
                  for tool in request.get('tools', [])}
    if 'write' in advertised:
        raise SmokeError('read-only reviewer advertised write')
    replies = [item for request in requests for item in request.get('messages', [])
               if item.get('role') == 'tool' and item.get('tool_call_id') == CALL_ID]
    errors = [item for item in replies if any(word in str(item.get('content', '')).lower()
              for word in ('not available', 'not found', 'invalid', 'denied', 'disabled', 'unknown tool'))]
    if not errors:
        raise SmokeError('no native error linked to the actual requested write tool call')
    if target.read_bytes() != original:
        raise SmokeError('read-only reviewer changed the protected target')
    return {'requested_tool': 'write', 'tool_call_id': CALL_ID, 'advertised': False,
            'native_error': errors[0]['content'], 'target_unchanged': True,
            'target_sha256': digest(original)}


def smoke(repo: Path, archive: Path | None, report: dict, timeout: int) -> None:
    system, machine = platform.system(), platform.machine().lower()
    if system not in RELEASES or machine not in ('amd64', 'x86_64'):
        raise SmokeError('supported native smoke platforms are Linux/Windows x64')
    name, expected_sha, executable = RELEASES[system]
    report.update({'schema_version': '1', 'status': 'running', 'runtime_version': VERSION,
                   'source_commit': SOURCE_COMMIT, 'platform': system, 'architecture': machine,
                   'runner_sha256': file_digest(Path(__file__)),
                   'cases': {}, 'commands': [],
                   'limitations': ['canned local provider; no real-model qualification',
                                   'no OS confinement, resume, delegation or compaction proof',
                                   'temporary instrumented data-only fixture; no host config adoption']})
    with tempfile.TemporaryDirectory(prefix='backbone-native-') as directory:
        root = Path(directory)
        if archive is None:
            archive = root / name
            download(f'https://github.com/anomalyco/opencode/releases/download/v{VERSION}/{name}', archive)
        binary = extract_verified(archive, root / 'bin', expected_sha, executable)
        report['archive'] = {'name': name, 'sha256': expected_sha,
                             'binary_sha256': file_digest(binary)}
        workspace = root / 'project'
        workspace.mkdir()
        expected = prepare_fixture(repo, workspace, report)
        env = isolated_environment(root / 'isolation')
        target = workspace / 'protected.txt'
        original = b'Protected native smoke target.\n'
        target.write_bytes(original)
        provider = CannedProvider(target)
        with provider.serve() as base_url:
            settings = {'model': 'backbone-smoke/smoke', 'small_model': 'backbone-smoke/smoke',
                        'enabled_providers': ['backbone-smoke'], 'share': 'disabled',
                        'provider': {'backbone-smoke': {'npm': '@ai-sdk/openai-compatible',
                                     'name': 'Local native smoke',
                                     'options': {'baseURL': base_url, 'apiKey': 'smoke-local-only'},
                                     'models': {'smoke': {'name': 'Canned smoke',
                                                'limit': {'context': 200000, 'output': 2048}}}}}}
            env['OPENCODE_CONFIG_CONTENT'] = json.dumps(settings)
            report['local_provider_config_sha256'] = digest(env['OPENCODE_CONFIG_CONTENT'].encode())
            successful(run_command(['git', 'init', '--quiet'], workspace, env, report, timeout))
            version = successful(run_command([str(binary), '--version'], workspace, env, report, timeout)).strip()
            if version != VERSION:
                raise SmokeError('actual native version differs from pin')
            report['cases']['version'] = {'status': 'passed', 'actual': version}
            roles = {}
            for role in ROLES:
                name = 'backbone-' + role
                raw = successful(run_command([str(binary), 'debug', 'agent', name], workspace, env, report, timeout))
                agent = json.loads(raw)
                if agent.get('name') != name or agent.get('mode') != 'primary':
                    raise SmokeError(f'native primary role not discovered: {name}')
                if role in ('planner', 'reviewer', 'triage'):
                    if any(agent.get('tools', {}).get(tool) is not False for tool in ('bash', 'edit', 'write', 'task')):
                        raise SmokeError(f'native read-only tool set differs: {name}')
                roles[name] = {'mode': agent['mode'], 'tools': agent.get('tools', {}),
                               'prompt_sha256': digest(agent.get('prompt', '').encode())}
            report['cases']['primary_roles'] = {'status': 'passed', 'roles': roles}
            # Native `run --agent unknown` may fall back. The controlled wrapper
            # must use this preflight and must not dispatch after its failure.
            before = len(provider.requests)
            missing = run_command([str(binary), 'debug', 'agent', 'backbone-smoke-missing'], workspace, env, report, timeout)
            if missing.code != 1 or 'not found' not in missing.stderr or len(provider.requests) != before:
                raise SmokeError('missing-role preflight did not stop before inference')
            report['cases']['missing_role_preflight'] = {'status': 'passed', 'expected_exit_code': 1,
                                                       'inference_requests': 0, 'run_dispatched': False}
            for nested in (False, True):
                before = len(provider.requests)
                cwd = workspace / 'nested' if nested else workspace
                successful(run_command([str(binary), 'run', '--agent', 'backbone-reviewer',
                                        '--model', 'backbone-smoke/smoke', '--format', 'json',
                                        '--title', 'Backbone native smoke', 'SMOKE_CONTEXT_ONLY'],
                                       cwd, env, report, timeout))
                evidence = check_loaded(provider.requests[before:], expected, nested=nested)
                report['cases']['nested_context' if nested else 'root_context'] = dict(evidence, status='passed')
            before = len(provider.requests)
            successful(run_command([str(binary), 'run', '--agent', 'backbone-reviewer',
                                    '--model', 'backbone-smoke/smoke', '--format', 'json',
                                    '--title', 'Backbone native tool boundary', 'SMOKE_TOOL_BOUNDARY'],
                                   workspace, env, report, timeout))
            evidence = check_denial(provider.requests[before:], target, original)
            report['cases']['read_only_tool_boundary'] = dict(evidence, status='passed')
            if provider.errors:
                raise SmokeError('local canned provider protocol error')
            report['provider_requests'] = len(provider.requests)
    report['status'] = 'passed'


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--archive', type=Path, help='optional cached archive; pin is still verified')
    parser.add_argument('--report', type=Path, default=Path('artifacts/opencode-native/report.json'))
    parser.add_argument('--timeout', type=int, default=60)
    args = parser.parse_args(argv)
    if not 1 <= args.timeout <= 120:
        parser.error('--timeout must be between 1 and 120 seconds')
    report: dict = {'status': 'failed', 'commands': []}
    started = time.monotonic()
    try:
        smoke(args.repo.resolve(), args.archive.resolve() if args.archive else None, report, args.timeout)
    except (SmokeError, OSError, ValueError, tarfile.TarError, zipfile.BadZipFile) as error:
        report['status'] = 'failed'
        report['error'] = str(error)
    report['seconds'] = round(time.monotonic() - started, 3)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f'Native smoke {report["status"]}; report: {args.report}')
    return 0 if report['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
