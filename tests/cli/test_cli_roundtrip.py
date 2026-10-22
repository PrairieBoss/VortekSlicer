"""Exercise Windows CLI help, shipped presets, slicing/export and 3MF round trips.

Run through CTest's RequiresApp label or pass --binary and --source-root.
All output/configuration stays in a fresh directory under --work-root. Logs and
input/output hashes are retained for diagnosis; no printer is contacted.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
import zipfile


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', type=Path, required=True)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--work-root', type=Path, required=True)
    parser.add_argument('--app-key', required=True)
    args = parser.parse_args()
    binary = args.binary.resolve()
    if not binary.is_file():
        print(f'SKIP: application binary not found: {binary}')
        return 77
    source = args.source_root.resolve()
    args.work_root.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix='cli-roundtrip-', dir=args.work_root)).resolve()
    profiles = source / 'resources/profiles/BBL'
    inputs = [source / 'tests/data/test_stl/ASCII/20mmbox-LF.stl',
              profiles / 'machine/Bambu Lab P1S 0.4 nozzle.json',
              profiles / 'process/0.20mm Standard @BBL X1C.json',
              profiles / 'filament/Bambu PLA Basic @BBL P1S 0.4 nozzle.json']
    dll = binary.with_name('OrcaSlicer.dll')
    summary = {'binary': str(binary), 'binary_sha256': sha256(binary),
               'application_dll_sha256': sha256(dll) if dll.is_file() else None,
               'inputs': {str(path): sha256(path) for path in inputs}, 'stages': []}

    def save_summary():
        (work / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')

    def run(tag, options):
        output = work / tag
        output.mkdir()
        command = [str(binary), '--datadir', str(output / 'datadir'), *map(str, options)]
        started = time.monotonic()
        with (output / 'stdout.log').open('wb') as log:
            result = subprocess.run(command, cwd=binary.parent, stdin=subprocess.DEVNULL,
                                    stdout=log, stderr=subprocess.STDOUT, timeout=300,
                                    creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        summary['stages'].append({'tag': tag, 'command': command, 'exit': result.returncode,
                                  'seconds': round(time.monotonic() - started, 3)})
        save_summary()
        if result.returncode:
            print((output / 'stdout.log').read_text(encoding='utf-8', errors='replace')[-12000:])
            raise RuntimeError(f'{tag}: application exited {result.returncode}')
        return output

    try:
        output = run('help', ['--help'])
        check(args.app_key + '-' in (output / 'stdout.log').read_text(encoding='utf-8', errors='replace'),
              'CLI help does not identify the selected product')
        initial = work / 'initial'
        run('initial', ['--load-settings', str(inputs[1]) + ';' + str(inputs[2]),
                        '--load-filaments', inputs[3], '--slice', '0', '--outputdir', initial,
                        '--export-3mf', 'project.3mf', inputs[0]])
        roundtrip = work / 'roundtrip'
        run('roundtrip', ['--slice', '0', '--outputdir', roundtrip,
                          '--export-3mf', 'project.3mf', initial / 'project.3mf'])
        configs, metrics = [], []
        for output in (initial, roundtrip):
            gcodes = list(output.glob('*.gcode'))
            check(len(gcodes) == 1, f'{output.name}: expected one exported G-code file')
            gcode = gcodes[0].read_text(encoding='utf-8', errors='replace')
            extrusion_moves = len(re.findall(r'^G[01]\s+[^;\n]*\b[XY][-+0-9.]+[^;\n]*\bE[-+0-9.]+', gcode, re.M))
            temperatures = re.findall(r'^M(?:104|109|140|190)\b[^;\n]*', gcode, re.M)
            check(extrusion_moves > 0, f'{output.name}: missing extrusion toolpaths')
            check(temperatures, f'{output.name}: missing temperature setup')
            with zipfile.ZipFile(output / 'project.3mf') as archive:
                check(archive.testzip() is None, f'{output.name}: corrupt project archive')
                config = json.loads(archive.read('Metadata/project_settings.config'))
                vertices = sum(sum(1 for element in ET.fromstring(archive.read(name)).iter()
                                   if element.tag.endswith('}vertex'))
                               for name in archive.namelist() if name.endswith('.model'))
                check(vertices > 0, f'{output.name}: missing saved model geometry')
            configs.append(config)
            metrics.append((extrusion_moves, sorted(temperatures), vertices))
            summary[output.name] = {'gcode_sha256': sha256(gcodes[0]),
                                    'project_sha256': sha256(output / 'project.3mf'),
                                    'extrusion_moves': extrusion_moves, 'model_vertices': vertices}
        for key in ('printer_settings_id', 'print_settings_id', 'filament_settings_id',
                    'layer_height', 'nozzle_diameter'):
            check(key in configs[0] and configs[0][key] == configs[1].get(key),
                  f'Project setting did not survive round trip: {key}')
        check(metrics[0] == metrics[1], 'Re-slicing changed toolpath count, temperatures or vertex count')
        for path in inputs:
            check(sha256(path) == summary['inputs'][str(path)], f'Input fixture modified: {path}')
        summary['result'] = 'passed'
        print('PASS: CLI identity, shipped profiles, cube slicing, G-code export and 3MF re-slicing')
        return 0
    except (OSError, RuntimeError, ValueError, zipfile.BadZipFile, ET.ParseError, subprocess.TimeoutExpired) as error:
        summary['result'] = 'failed'
        summary['error'] = str(error)
        print(f'FAIL: {error}', file=sys.stderr)
        return 1
    finally:
        save_summary()
        print(f'Evidence: {work / "summary.json"}')


if __name__ == '__main__':
    sys.exit(main())
