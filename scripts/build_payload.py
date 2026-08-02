#!/usr/bin/env python3
"""Build exact-build SquashFS payloads for the synthetic host extension."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--module', required=True, type=Path)
    parser.add_argument('--kernel-release', required=True)
    parser.add_argument('--reefy-build-id', required=True)
    parser.add_argument('--kernel-abi-digest', required=True)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    output = args.output
    common = output / 'common-root'
    kernel = output / 'kernel-root'
    shutil.rmtree(output, ignore_errors=True)
    (common / 'usr/lib/reefy').mkdir(parents=True)
    module_dir = kernel / 'lib/modules' / args.kernel_release / 'extra'
    module_dir.mkdir(parents=True)
    shutil.copy2(root / 'scripts/activate', common / 'usr/lib/reefy/activate')
    (common / 'usr/lib/reefy/activate').chmod(0o755)
    shutil.copy2(args.module, module_dir / 'reefy_e2e_artifact.ko')

    config = {
        'artifact_schema': 1,
        'kind': 'host-extension',
        'name': 'e2e-host-extension',
        'version': '1',
        'architecture': 'x86_64',
        'publisher': 'reefyai',
        'activation_hook': 'usr/lib/reefy/activate',
        'reefy_build_id': args.reefy_build_id,
        'kernel_abi_digest': args.kernel_abi_digest,
        'kernel_release': args.kernel_release,
        'capabilities': ['e2e.kernel-module', 'e2e.cdi'],
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / 'config.json').write_text(
        json.dumps(config, indent=2, sort_keys=True) + '\n')
    for source, destination in (
            (common, output / 'common.squashfs'),
            (kernel, output / 'kernel.squashfs')):
        subprocess.run(
            ['mksquashfs', str(source), str(destination), '-noappend',
             '-comp', 'zstd', '-quiet'], check=True)


if __name__ == '__main__':
    main()
