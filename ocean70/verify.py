"""Launch a fresh offline test server, load the actual ZIP, measure biome connectivity and terrain."""
import json
import hashlib
import queue
import shutil
import subprocess
import threading
import time
import zipfile
from build import BASE, ROOT, OUT, RUNTIME, JDK, classpath


def main():
    asm = ROOT / 'ida26/test-agent/asm.jar'
    cp = classpath() + ';' + str(asm)
    subprocess.run([str(JDK / 'javac.exe'), '-cp', cp, str(BASE / 'OceanProbe.java'), str(BASE / 'OceanAgent.java')], check=True)
    agent = OUT / 'ocean-probe.jar'
    with zipfile.ZipFile(agent, 'w') as z:
        z.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\nPremain-Class: OceanAgent\n\n')
        for path in [*BASE.glob('OceanProbe*.class'), *BASE.glob('OceanAgent*.class')]:
            z.write(path, path.name)
    run = BASE / 'test-runtime' / str(int(time.time()))
    dp = run / 'world/datapacks'
    dp.mkdir(parents=True)
    shutil.copy2(OUT / 'Ocean70-Land30-Java-26.3.zip', dp / 'Ocean70.zip')
    (run / 'eula.txt').write_text('eula=true\n')
    (run / 'server.properties').write_text('\n'.join([
        'level-name=world', 'level-type=minecraft:normal', 'level-seed=73102631',
        'online-mode=false', 'server-ip=127.0.0.1', 'server-port=25589',
        'enable-query=false', 'enable-rcon=false', 'view-distance=2', 'simulation-distance=2',
        'max-tick-time=-1', 'generate-structures=true']) + '\n')
    report = OUT / 'engine-validation.json'
    # Preserve previous results; only this run's file is a completion signal.
    if report.exists():
        report.rename(OUT / f'engine-validation-{int(time.time())}.json')
    failure = OUT / 'probe-error.txt'
    if failure.exists():
        failure.unlink()
    cmd = [str(JDK / 'java.exe'), '-Xms256M', '-Xmx3G',
           '-javaagent:' + str(ROOT / 'ida26/test-agent/test-network.jar'),
           '-javaagent:' + str(agent), '-Docean70.output=' + str(OUT),
           '-cp', cp, 'net.minecraft.server.Main', 'nogui']
    p = subprocess.Popen(cmd, cwd=run, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
    lines = queue.Queue()
    def pump():
        for line in p.stdout:
            lines.put(line)
    threading.Thread(target=pump, daemon=True).start()
    start = time.time()
    stopping = False
    log_path = OUT / 'server-validation.log'
    try:
        with log_path.open('w', encoding='utf-8') as log:
            while time.time() - start < 600:
                try:
                    line = lines.get(timeout=.3)
                except queue.Empty:
                    line = ''
                if line:
                    log.write(line); log.flush()
                    if any(s in line for s in ['ERROR', 'OCEAN70', 'Done (', 'Exception', 'Failed']):
                        print(line.rstrip(), flush=True)
                if not stopping and (report.exists() or failure.exists()):
                    p.stdin.write('datapack list enabled\nstop\n'); p.stdin.flush()
                    stopping = True
                if p.poll() is not None:
                    break
    finally:
        if p.poll() is None:
            p.stdin.write('stop\n'); p.stdin.flush()
            try:
                p.wait(timeout=30)
            except subprocess.TimeoutExpired:
                p.kill(); p.wait()
    assert report.exists(), f'Probe did not complete; inspect {log_path}'
    log = log_path.read_text(encoding='utf-8')
    errors = [l for l in log.splitlines() if any(s in l for s in ['Failed to parse', 'Failed to load', 'Unknown or incomplete', 'Exception in thread'])]
    assert not errors, '\n'.join(errors)
    data = json.loads(report.read_text(encoding='utf-8'))
    config = json.loads((BASE / 'settings.json').read_text(encoding='utf-8'))
    target = config['target_ocean_fraction']
    assert abs(data['mean_ocean_fraction'] - target) < .02, data['mean_ocean_fraction']
    assert data['terrain_columns']['deep_ocean_columns_above_sea'] == 0, data['terrain_columns']
    for row in data['seeds']:
        land = row['land_components']
        bound = config['continent_cell_blocks'] + 2 * config['maximum_warp_blocks'] + 32
        assert land['maximum_span_across_all_components'] < bound, row
        assert land['largest_sampled_area_blocks2'] < bound * bound, row
    data['datapack_sha256'] = hashlib.sha256((dp / 'Ocean70.zip').read_bytes()).hexdigest()
    with zipfile.ZipFile(dp / 'Ocean70.zip') as z:
        executable = {name: (json.loads(z.read(name)) if name.endswith('.json') or name == 'pack.mcmeta'
                             else z.read(name).decode('utf-8'))
                      for name in z.namelist() if name.startswith('data/') or name == 'pack.mcmeta'}
    data['runtime_content_sha256'] = hashlib.sha256(json.dumps(executable, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    data['verification_passed'] = True
    report.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Passed: actual datapack load, mean ratio, and continent size limits.')


if __name__ == '__main__':
    main()
