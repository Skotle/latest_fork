"""Build local Continents presets from the user-provided original ZIP."""
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
PRESETS = {
    'balanced': (140, 125, 120, 120),
    'archipelago': (85, 140, 140, 150),
    'grand': (200, 150, 100, 85),
}
LABELS = ['대륙 크기', '시작 섬 크기', '주변 섬 크기', '주변 섬 생성 영향']


def locate(document, path):
    node = document
    parts = path.split('/')
    for part in parts[:-1]:
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node, int(parts[-1]) if isinstance(node, list) else parts[-1]


def repair_config(config):
    methods = config['config']['methods']
    for name, method in methods.items():
        for accessor in method['accessors']:
            if name.startswith('continent_scale'):
                accessor['value_path'] = 'left/input/input/xz_scale'
            elif name.startswith('spawn_island_size'):
                old = accessor['value_path']
                accessor['value_path'] = ('input/input/left/xz_scale' if old == 'argument/argument1/xz_scale'
                                          else 'input/input/right/left/xz_scale')
            elif name.startswith('island_scale'):
                accessor['value_path'] = 'right/right/input/right/input/left/input/input/xz_scale'
    widgets = config['config']['widgets']
    widgets[0]['text'] = 'Continents 지형 설정'
    widgets[1]['text'] = '원작: Stardust Labs · 개인 사용 개선판. 크기는 면적 기준 설정값이며 실제 지형은 시드에 따라 달라집니다.'
    for widget in widgets:
        if widget['type'] == 'heading':
            widget['text'] = '큰 생물 군계' if 'Large' in widget['text'] else '기본 월드'
    sliders = [w for w in widgets if w['type'] == 'slider']
    for index, widget in enumerate(sliders):
        widget['text'] = LABELS[index % 4] + (' (큰 생물 군계)' if index >= 4 else '')


def validate(files):
    config = files['dpconfig.json']['config']
    checked = 0
    for method in config['methods'].values():
        for accessor in method['accessors']:
            paths = accessor['file_path']
            for path in ([paths] if isinstance(paths, str) else paths):
                parent, key = locate(files[path], accessor['value_path'])
                assert isinstance(parent[key], (int, float)), (path, key)
                checked += 1
    for path, document in files.items():
        if '/density_function/' in path and isinstance(document, dict) and 'spline' in document:
            points = document['spline']['points']
            assert all(a['location'] < b['location'] for a, b in zip(points, points[1:])), path
    def references(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key == 'noise' and isinstance(value, str) and value.startswith('continents:'):
                    assert 'data/continents/worldgen/noise/' + value.split(':', 1)[1] + '.json' in files, value
                else:
                    references(value)
        elif isinstance(node, list):
            for value in node:
                references(value)
        elif isinstance(node, str) and node.startswith('continents:'):
            assert 'data/continents/worldgen/density_function/' + node.split(':', 1)[1] + '.json' in files, node
    for path, document in files.items():
        if '/density_function/' in path:
            references(document)
    return checked


def build(source):
    with zipfile.ZipFile(source) as archive:
        raw = {i.filename: archive.read(i) for i in archive.infolist() if not i.is_dir()}
    original = {p: json.loads(b) for p, b in raw.items() if p.endswith('.json') or p == 'pack.mcmeta'}
    repair_config(original['dpconfig.json'])
    checked = validate(original)
    output = ROOT / 'output'
    output.mkdir(exist_ok=True)
    report = {'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'accessor_targets_checked': checked, 'presets': {}}
    for preset, values in PRESETS.items():
        files = copy.deepcopy(original)
        config = files['dpconfig.json']['config']
        sliders = [w for w in config['widgets'] if w['type'] == 'slider']
        changes = []
        for index, widget in enumerate(sliders):
            percent = values[index % 4]
            assert widget['value']['range'][0] <= percent <= widget['value']['range'][1]
            widget['value']['default'] = percent
            method = config['methods'][widget['method']]
            ratio = percent / 100
            adjustment = math.sqrt(ratio) if method['value']['function'] == 'square_root' else ((ratio - 1) * (0.5 if ratio < 1 else 0.25))
            for accessor in method['accessors']:
                paths = accessor['file_path']
                for path in ([paths] if isinstance(paths, str) else paths):
                    parent, key = locate(files[path], accessor['value_path'])
                    before = parent[key]
                    parent[key] = before / adjustment if accessor['method'] == 'divide' else before + adjustment
                    changes.append({'file': path, 'path': accessor['value_path'], 'before': before, 'after': parent[key]})
        validate(files)
        target = output / f'Continents-Improved-{preset}-26.3.zip'
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
            for path, content in raw.items():
                data = (json.dumps(files[path], ensure_ascii=False, indent=2) + '\n').encode('utf-8') if path in files else content
                archive.writestr(path, data)
        with zipfile.ZipFile(target) as archive:
            assert archive.testzip() is None
            assert 'pack.mcmeta' in archive.namelist()
            for path in files:
                json.loads(archive.read(path))
        report['presets'][preset] = {'file': target.name, 'settings_percent': values, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest(), 'changes': changes}
        print(f'OK: {target.name} ({len(changes)} value changes)')
    (output / 'validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path.home() / 'Downloads' / 'Continents_v1.2.1+26.3.zip')
    build(parser.parse_args().source)
