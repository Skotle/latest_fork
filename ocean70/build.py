"""Build a minimal, calibrated Minecraft Java 26.3 worldgen datapack."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import zipfile

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
RUNTIME = ROOT / '.tools/boss-model-test'
JDK = RUNTIME / 'jdk/jdk-25.0.4.1/bin'
ENGINE = RUNTIME / 'versions/26.3/server-26.3.jar'
OUT = BASE / 'output'
PACK = BASE / 'datapack'


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def classpath():
    return os.pathsep.join(map(str, [ENGINE, *sorted((RUNTIME / 'libraries').rglob('*.jar')), BASE]))


def binary(kind, left, right):
    return {'type': 'minecraft:' + kind, 'left': left, 'right': right}


def channel_mask(config):
    # Continuous warped cells. Warp is bounded, so cells cannot grow without limit.
    # The floor discontinuity is removed by folding the remainder into a triangle.
    def distance(axis, noise_id, scale):
        period = config['continent_cell_blocks']
        half = period / 2
        coord = {'type': 'minecraft:gradient', 'axis': axis, 'tiling': 'repeat',
                 'from_coordinate': 0, 'to_coordinate': period,
                 'from_value': 0, 'to_value': period}
        warp_noise = {'type': 'minecraft:noise', 'noise': noise_id, 'xz_scale': scale, 'y_scale': 0.0}
        scaled = binary('mul', config['warp_noise_strength'], warp_noise)
        # Smooth bounded warp: q / sqrt(1+q²). Hard clipping would make long straight coastlines.
        bounded = binary('div', scaled, {'type': 'minecraft:sqrt',
            'input': binary('add', 1.0, {'type': 'minecraft:square', 'input': scaled})})
        warp = binary('mul', config['maximum_warp_blocks'], bounded)
        warped = binary('add', binary('add', coord, half), warp)
        remainder = binary('sub', warped, {'type': 'minecraft:floor', 'input': warped, 'multiple': period})
        return binary('sub', half, {'type': 'minecraft:abs', 'input': binary('sub', remainder, half)})
    d = binary('min', distance('x', 'minecraft:temperature', 1.2),
               distance('z', 'minecraft:erosion', .75))
    return {'type': 'minecraft:clamp', 'input': binary('div',
            binary('sub', d, config['ocean_channel_half_width_blocks']), config['coast_transition_blocks']),
            'min': -.8, 'max': 1.0}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--calibrate', action='store_true', help='Recompute bias with the official Java runtime')
    args = ap.parse_args()
    config_path = BASE / 'settings.json'
    config = json.loads(config_path.read_text(encoding='utf-8'))
    assert 0 < config['target_ocean_fraction'] < 1
    assert isinstance(config['continent_cell_blocks'], int) and config['continent_cell_blocks'] > 0
    assert config['maximum_warp_blocks'] >= 0 and config['coast_transition_blocks'] > 0
    OUT.mkdir(exist_ok=True)
    noise = {'type': 'minecraft:noise', 'noise': 'minecraft:continentalness',
             'shift_x': 'minecraft:shift_x', 'shift_z': 'minecraft:shift_z',
             'xz_scale': config['continental_noise_scale'], 'y_scale': 0.0}
    raw = OUT / 'raw-continents.json'
    write_json(raw, noise)
    mask_path = OUT / 'channel-mask.json'
    mask = channel_mask(config)
    write_json(mask_path, mask)
    calibration = OUT / 'calibration.json'
    previous = json.loads(calibration.read_text(encoding='utf-8')) if calibration.exists() else {}
    recipe_sha = hashlib.sha256(json.dumps({'noise': noise, 'mask': mask}, sort_keys=True).encode()).hexdigest()
    if args.calibrate or previous.get('settings') != config or previous.get('recipe_sha256') != recipe_sha:
        subprocess.run([str(JDK / 'javac.exe'), '-cp', classpath(), str(BASE / 'ContinentsSample.java')], check=True)
        subprocess.run([str(JDK / 'java.exe'), '-Xmx2G', '-cp', classpath(), 'ContinentsSample',
                        str(raw), str(mask_path), str(calibration), str(config_path)], check=True, cwd=OUT)
        calibrated = json.loads(calibration.read_text(encoding='utf-8'))
        calibrated['recipe_sha256'] = recipe_sha
        write_json(calibration, calibrated)
    bias = json.loads(calibration.read_text(encoding='utf-8'))['bias']
    write_json(PACK / 'pack.mcmeta', {'pack': {'min_format': [121, 0], 'max_format': [121, 0],
               'description': 'Ocean 70 / Land 30 — calibrated 10,000 x 10,000 Overworld (Java 26.3)'}})
    # Shared continents reference feeds both terrain splines and biome climate.
    write_json(PACK / 'data/minecraft/worldgen/density_function/overworld/continents.json', {
        'type': 'minecraft:cache', 'input': {'type': 'minecraft:clamp',
        'input': binary('min', binary('add', bias, noise), mask), 'min': -1.0, 'max': 1.0}})
    functions = PACK / 'data/ocean70/function'
    functions.mkdir(parents=True, exist_ok=True)
    (functions / 'border_10000.mcfunction').write_text(
        '# Optional: applies only when an administrator explicitly calls this function.\n'
        'execute in minecraft:overworld run worldborder center 0 0\n'
        'execute in minecraft:overworld run worldborder set 10000\n', encoding='utf-8')
    (functions / 'info.mcfunction').write_text(
        'tellraw @s {"text":"Ocean70: Java 26.3 / land ~30%, ocean ~70% / new Overworld chunks / optional border: /function ocean70:border_10000","color":"aqua"}\n', encoding='utf-8')
    archive = OUT / 'Ocean70-Land30-Java-26.3.zip'
    if (BASE / 'README.ko.md').exists():
        (PACK / 'README.ko.md').write_bytes((BASE / 'README.ko.md').read_bytes())
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for path in sorted(PACK.rglob('*')):
            if path.is_file():
                z.writestr(zipfile.ZipInfo(path.relative_to(PACK).as_posix(), (2026, 10, 12, 0, 0, 0)),
                           path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED)
    write_json(OUT / 'build.json', {'archive': archive.name, 'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
               'minecraft_version': '26.3', 'data_pack_version': [121, 0], 'continentalness_bias': bias,
               'settings': config,
               'maximum_continentalness_component_span_blocks': config['continent_cell_blocks'] + 2 * config['maximum_warp_blocks'],
               'files': len(list(PACK.rglob('*.*')))})
    print(f'Built {archive}; bias={bias}')


if __name__ == '__main__':
    main()
