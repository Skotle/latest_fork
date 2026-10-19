"""Build star-shaped continents with a connected exterior ocean field."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
SOURCE = Path.home() / 'Downloads/Continents_v1.2.1+26.3.zip'
NS = 'continents:connected/'


def op(kind, a, b):
    return {'type': 'minecraft:' + kind, 'left': a, 'right': b}


def unary(kind, value):
    return {'type': 'minecraft:' + kind, 'input': value}


def clamp(value, low, high):
    return dict(unary('clamp', value), min=low, max=high)


def fields(period=3600, radius=1050, variation=180, coast=350):
    assert 0 < variation < radius and radius + variation < period / 2
    result = {}
    for axis in ('x', 'z'):
        local = {'type': 'minecraft:gradient', 'axis': axis, 'tiling': 'repeat',
                 'from_coordinate': -period // 2, 'to_coordinate': period // 2,
                 'from_value': -period / 2, 'to_value': period / 2}
        result['d' + axis] = local
        absolute = {'type': 'minecraft:gradient', 'axis': axis,
                    'from_coordinate': -30000000, 'to_coordinate': 30000000,
                    'from_value': -30000, 'to_value': 30000}
        result['center_' + axis] = op('sub', absolute, op('mul', .001, NS + 'd' + axis))
    result['distance'] = unary('sqrt', op('add', unary('square', NS + 'dx'), unary('square', NS + 'dz')))
    # At the exact centre the denominator is protected. The entire protected
    # core lies inside the minimum land radius, so topology is unaffected.
    denominator = op('max', 1, NS + 'distance')
    result['radius'] = op('add', radius, op('mul', variation, clamp({
        'type': 'minecraft:noise', 'noise': 'minecraft:erosion',
        'xz_scale': 0.0, 'y_scale': 0.0, 'shift_y': 0.0,
        'shift_x': op('add', NS + 'center_x', op('mul', 8, op('div', NS + 'dx', denominator))),
        'shift_z': op('add', NS + 'center_z', op('mul', 8, op('div', NS + 'dz', denominator))),
    }, -1, 1)))
    result['continents'] = unary('cache', {'type': 'minecraft:slice', 'axis': 'y', 'coordinate': 0,
        'input': clamp(op('add', -.19, op('div', op('sub', NS + 'radius', NS + 'distance'), coast)), -1, 1)})
    return result


def main():
    generated = fields()
    output = ROOT / 'output'
    output.mkdir(exist_ok=True)
    target = output / 'Continents-Connected-Ocean-26.3.zip'
    with zipfile.ZipFile(SOURCE) as archive:
        raw = {i.filename: archive.read(i) for i in archive.infolist() if not i.is_dir()}
    # The old sliders target the original noise pipeline and would be misleading.
    raw.pop('dpconfig.json', None)
    for name, value in generated.items():
        raw['data/continents/worldgen/density_function/connected/' + name + '.json'] = json.dumps(value, indent=2).encode()
    for preset in ('overworld', 'overworld_large_biomes'):
        raw[f'data/minecraft/worldgen/density_function/{preset}/continents.json'] = json.dumps(NS + 'continents').encode()
    metadata = json.loads(raw['pack.mcmeta'])
    metadata['pack']['description'].append({'text': '\nConnected ocean / local edition', 'color': 'aqua'})
    raw['pack.mcmeta'] = json.dumps(metadata, ensure_ascii=False, indent=2).encode('utf-8')
    raw['CONNECTED-OCEAN.ko.md'] = (ROOT / 'CONNECTED-OCEAN.ko.md').read_bytes()
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(raw.items()):
            archive.writestr(name, data)
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        for name in archive.namelist():
            if name.endswith('.json') or name == 'pack.mcmeta':
                json.loads(archive.read(name))
    report = {'file': target.name, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
              'cell_blocks': 3600, 'land_radius_min_blocks': 870, 'land_radius_max_blocks': 1230,
              'minimum_gap_between_land_envelopes_blocks': 1140,
              'ocean_threshold': -.19,
              'topology': 'Within each cell radius is a function of direction and cell centre only; land is star-shaped. Disjoint land envelopes leave a connected exterior ocean.',
              'small_lakes': 'allowed; vanilla terrain and lake features retained',
              'validation': 'JSON and ZIP checks; independent expression sampling in verify_connected.py',
              'minecraft_runtime_verified': False}
    (output / 'connected-build.json').write_text(json.dumps(report, indent=2) + '\n')
    print(target)


if __name__ == '__main__':
    main()
