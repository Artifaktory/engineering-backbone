"""Portable failure-path tests; native CLI evidence is a separate command."""
from __future__ import annotations

import io
import json
from pathlib import Path
import stat
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch
import urllib.request
import zipfile

from scripts import opencode_native_smoke as smoke


class NativeSmokeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='native-smoke-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def tar(self, members):
        archive = self.root / 'test.tar.gz'
        with tarfile.open(archive, 'w:gz') as bundle:
            for name, content, kind in members:
                entry = tarfile.TarInfo(name)
                entry.type = kind
                entry.size = len(content) if kind == tarfile.REGTYPE else 0
                if kind == tarfile.SYMTYPE:
                    entry.linkname = '../outside'
                bundle.addfile(entry, io.BytesIO(content))
        return archive

    def test_wrong_digest_never_extracts(self):
        archive = self.tar([('opencode', b'binary', tarfile.REGTYPE)])
        with self.assertRaisesRegex(smoke.SmokeError, 'SHA-256 mismatch'):
            smoke.extract_verified(archive, self.root / 'bin', '0' * 64, 'opencode')
        self.assertFalse((self.root / 'bin').exists())

    def test_tar_accepts_only_one_regular_root_binary(self):
        for members in ([('../opencode', b'bad', tarfile.REGTYPE)],
                        [('opencode', b'', tarfile.SYMTYPE)],
                        [('opencode', b'valid', tarfile.REGTYPE), ('extra', b'bad', tarfile.REGTYPE)]):
            with self.subTest(members=members):
                archive = self.tar(members)
                with self.assertRaisesRegex(smoke.SmokeError, 'regular root|root executable'):
                    smoke.extract_verified(archive, self.root / 'bin', smoke.file_digest(archive), 'opencode')
        archive = self.tar([('opencode', b'valid', tarfile.REGTYPE)])
        binary = smoke.extract_verified(archive, self.root / 'bin', smoke.file_digest(archive), 'opencode')
        self.assertEqual(binary.read_bytes(), b'valid')

    def test_zip_accepts_regular_binary_rejects_symlink_and_extra_paths(self):
        for kind in ('regular', 'symlink', 'extra'):
            archive = self.root / 'test.zip'
            with zipfile.ZipFile(archive, 'w') as bundle:
                item = zipfile.ZipInfo('opencode.exe')
                item.create_system = 3
                item.external_attr = ((stat.S_IFLNK if kind == 'symlink' else stat.S_IFREG) | 0o700) << 16
                bundle.writestr(item, b'valid')
                if kind == 'extra':
                    bundle.writestr('../outside', b'bad')
            if kind == 'regular':
                binary = smoke.extract_verified(archive, self.root / 'bin', smoke.file_digest(archive), 'opencode.exe')
                self.assertEqual(binary.read_bytes(), b'valid')
            else:
                with self.assertRaises(smoke.SmokeError):
                    smoke.extract_verified(archive, self.root / 'bin', smoke.file_digest(archive), 'opencode.exe')

    def test_environment_drops_host_auth_overrides_and_hooks(self):
        env = smoke.isolated_environment(self.root, {
            'PATH': '/bin', 'SystemRoot': r'C:\Windows', 'OPENAI_API_KEY': 'secret',
            'OPENCODE_CONFIG': '/host/config', 'OPENCODE_PERMISSION': '{}',
            'GITHUB_TOKEN': 'secret', 'NODE_OPTIONS': '--require injected.js',
            'GIT_CONFIG_COUNT': '1', 'HOME': '/host/home', 'HTTPS_PROXY': 'http://host',
        })
        self.assertEqual(env['PATH'], '/bin')
        self.assertEqual(env['SystemRoot'], r'C:\Windows')
        self.assertEqual(env['HOME'], str(self.root / 'home'))
        for key in ('OPENAI_API_KEY', 'OPENCODE_CONFIG', 'OPENCODE_PERMISSION',
                    'GITHUB_TOKEN', 'NODE_OPTIONS', 'GIT_CONFIG_COUNT'):
            self.assertNotIn(key, env)
        self.assertEqual(env['OPENCODE_PURE'], '1')

    def test_command_timeout_and_output_bound_are_reported(self):
        for command, timeout, expected in [
            ('import time; time.sleep(20)', 0.1, 'timeout'),
            ('print("x" * 10000)', 5, 'output limit'),
        ]:
            report = {}
            with self.subTest(expected=expected), patch.object(smoke, 'MAX_OUTPUT', 1024):
                with self.assertRaisesRegex(smoke.SmokeError, expected):
                    smoke.run_command([sys.executable, '-c', command], self.root,
                                      smoke.isolated_environment(self.root), report, timeout)
                self.assertEqual(len(report['commands']), 1)
                self.assertIn(expected, report['commands'][0]['failure'])

    def test_loaded_context_requires_one_complete_selected_agent_request(self):
        expected = {'AGENTS.md': 'root rules', 'policy/core.md': 'core rules'}
        payload = {'messages': [{'role': 'system', 'content': smoke.ROLE_MARKER + '\nroot rules\ncore rules\n' + smoke.NESTED_MARKER}]}
        self.assertTrue(smoke.check_loaded([payload], expected, nested=True)['nested_marker'])
        for text in ('root rules\ncore rules', smoke.ROLE_MARKER + '\nroot rules',
                     smoke.ROLE_MARKER + '\nroot rules\ncore rules'):
            with self.subTest(text=text), self.assertRaises(smoke.SmokeError):
                smoke.check_loaded([{'messages': [{'content': text}]}], expected, nested=True)
        split = [{'messages': [{'content': smoke.ROLE_MARKER + '\n' + value}]} for value in expected.values()]
        with self.assertRaises(smoke.SmokeError):
            smoke.check_loaded(split, expected, nested=False)

    def test_fixture_copies_declared_inputs_and_records_instrumentation(self):
        repo, workspace = self.root / 'repo', self.root / 'fixture'
        repo.mkdir()
        config = {'$schema': 'https://opencode.ai/config.json',
                  'instructions': ['AGENTS.md', 'policy.json'], 'permission': {'*': 'deny'}}
        (repo / 'opencode.json').write_text(json.dumps(config), encoding='utf-8')
        (repo / 'AGENTS.md').write_text('Actual source instructions.\n', encoding='utf-8')
        (repo / 'policy.json').write_text('{"policy": "unchanged"}\n', encoding='utf-8')
        for name in ([f'.opencode/agents/backbone-{role}.md' for role in smoke.ROLES]
                     + [f'.opencode/skills/{skill}/SKILL.md' for skill in smoke.SKILLS]):
            path = repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('Fixture data.\n', encoding='utf-8')
        ignored = repo / '.opencode/plugins/unrelated.txt'
        ignored.parent.mkdir(parents=True)
        ignored.write_text('Not a declared smoke input.\n', encoding='utf-8')
        report = {}
        expected = smoke.prepare_fixture(repo, workspace, report)
        self.assertIn('BACKBONE_NATIVE_SMOKE_INSTRUCTION_', expected['AGENTS.md'])
        self.assertEqual(expected['policy.json'], '{"policy": "unchanged"}')
        self.assertFalse((workspace / '.opencode/plugins').exists())
        hashes = report['inputs']['AGENTS.md']
        self.assertNotEqual(hashes['source_sha256'], hashes['fixture_sha256'])
        config['instructions'] = ['../escape.md']
        (repo / 'opencode.json').write_text(json.dumps(config), encoding='utf-8')
        with self.assertRaisesRegex(smoke.SmokeError, 'invalid source input path'):
            smoke.prepare_fixture(repo, self.root / 'invalid', {})

    def boundary(self):
        initial = {'messages': [{'role': 'system', 'content': smoke.ROLE_MARKER},
                                {'role': 'user', 'content': 'SMOKE_TOOL_BOUNDARY'}],
                   'tools': [{'function': {'name': 'read'}}]}
        reply = {'role': 'tool', 'tool_call_id': smoke.CALL_ID,
                 'content': 'Error: Tool write is not available'}
        return initial, reply

    def test_unchanged_file_alone_is_not_native_denial_evidence(self):
        target = self.root / 'protected.txt'
        original = b'unchanged'
        target.write_bytes(original)
        initial, reply = self.boundary()
        with self.assertRaisesRegex(smoke.SmokeError, 'no native error'):
            smoke.check_denial([initial], target, original)
        reply['tool_call_id'] = 'wrong-call'
        with self.assertRaisesRegex(smoke.SmokeError, 'no native error'):
            smoke.check_denial([initial, {'messages': [reply]}], target, original)
        reply['tool_call_id'] = smoke.CALL_ID
        result = smoke.check_denial([initial, {'messages': [reply]}], target, original)
        self.assertTrue(result['target_unchanged'])
        target.write_bytes(b'changed')
        with self.assertRaisesRegex(smoke.SmokeError, 'changed the protected'):
            smoke.check_denial([initial, {'messages': [reply]}], target, original)

    def test_success_reply_or_advertised_write_cannot_pass_denial(self):
        target = self.root / 'protected.txt'
        target.write_bytes(b'original')
        initial, reply = self.boundary()
        reply['content'] = 'Write succeeded'
        with self.assertRaisesRegex(smoke.SmokeError, 'no native error'):
            smoke.check_denial([initial, {'messages': [reply]}], target, b'original')
        initial['tools'].append({'function': {'name': 'write'}})
        with self.assertRaisesRegex(smoke.SmokeError, 'advertised write'):
            smoke.check_denial([initial], target, b'original')

    def test_local_peer_requests_actual_tool_then_stops_after_linked_reply(self):
        provider = smoke.CannedProvider(self.root / 'target')
        initial, reply = self.boundary()
        chunks = provider.chunks(initial)
        call = chunks[0]['choices'][0]['delta']['tool_calls'][0]
        self.assertEqual(call['id'], smoke.CALL_ID)
        self.assertEqual(call['function']['name'], 'write')
        self.assertEqual(json.loads(call['function']['arguments'])['filePath'], str(self.root / 'target'))
        initial['messages'].append(reply)
        self.assertEqual(provider.chunks(initial)[1]['choices'][0]['finish_reason'], 'stop')

    def test_local_http_provider_records_real_request_and_returns_stream(self):
        provider = smoke.CannedProvider(self.root / 'target')
        payload = {'messages': [{'role': 'user', 'content': 'context check'}], 'stream': True}
        with provider.serve() as url:
            request = urllib.request.Request(url + '/chat/completions',
                                             data=json.dumps(payload).encode(),
                                             headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(request, timeout=5) as response:
                self.assertIn(b'data: [DONE]', response.read())
        self.assertEqual(provider.requests, [payload])
        self.assertEqual(provider.errors, [])


if __name__ == '__main__':
    unittest.main()
