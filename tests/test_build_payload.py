import runpy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


class BuildPayloadTests(unittest.TestCase):
    def test_squashfs_layers_are_reproducible(self):
        root = Path(__file__).resolve().parents[1]
        module = root / 'module/reefy_e2e_artifact.c'
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'output'
            argv = [
                'build_payload.py',
                '--module', str(module),
                '--kernel-release', '6.18.40',
                '--reefy-build-id', 'a' * 64,
                '--kernel-abi-digest', f'sha256:{"b" * 64}',
                '--output', str(output),
            ]
            with mock.patch.object(sys, 'argv', argv), mock.patch(
                    'subprocess.run') as run:
                runpy.run_path(
                    str(root / 'scripts/build_payload.py'),
                    run_name='__main__')

        self.assertEqual(run.call_count, 2)
        for call in run.call_args_list:
            command = call.args[0]
            self.assertIn('-all-root', command)
            self.assertIn('-all-time', command)
            self.assertEqual(command[command.index('-all-time') + 1], '0')
            self.assertIn('-mkfs-time', command)
            self.assertEqual(command[command.index('-mkfs-time') + 1], '0')
            self.assertIn('-no-xattrs', command)
            self.assertTrue(call.kwargs['check'])


if __name__ == '__main__':
    unittest.main()
