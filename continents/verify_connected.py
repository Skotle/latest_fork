"""Validate the generated density expression with the local official 26.3 engine."""
import json
import os
from pathlib import Path
import subprocess
import zipfile
from build_connected import ROOT, NS


def main():
    workspace = ROOT.parent
    jdk = workspace / '.tools/jdk25/jdk-25.0.4.1+1/bin'
    out = ROOT / 'output'
    runtime = ROOT / '.runtime'
    runtime.mkdir(exist_ok=True)
    with zipfile.ZipFile(workspace / '.tools/paper263/cache/mojang_26.3.jar') as bundle:
        entry = next(n for n in bundle.namelist() if n.startswith('META-INF/versions/') and n.endswith('.jar'))
        engine = runtime / 'server-26.3.jar'
        engine.write_bytes(bundle.read(entry))
    with zipfile.ZipFile(out / 'Continents-Connected-Ocean-26.3.zip') as archive:
        fields = {name[len('data/continents/worldgen/density_function/connected/'):-5]: json.loads(archive.read(name))
                  for name in archive.namelist() if name.startswith('data/continents/worldgen/density_function/connected/')}
    def expand(value):
        if isinstance(value, str) and value.startswith(NS):
            return expand(fields[value[len(NS):]])
        if isinstance(value, dict):
            return {key: expand(child) for key, child in value.items()}
        if isinstance(value, list):
            return [expand(child) for child in value]
        return value
    expression = out / 'connected-expression.json'
    expression.write_text(json.dumps(expand(fields['continents'])))
    cp = os.pathsep.join(map(str, [engine, *sorted((workspace / '.tools/paper263/libraries').rglob('*.jar')), runtime]))
    subprocess.run([str(jdk / 'javac.exe'), '-cp', cp, '-d', str(runtime), str(ROOT / 'ConnectedSample.java')], check=True)
    subprocess.run([str(jdk / 'java.exe'), '-Xmx2G', '-cp', cp, 'ConnectedSample', str(expression),
                    str(out / 'connected-engine-validation.json')], check=True, cwd=runtime)
    report_path = out / 'connected-build.json'
    report = json.loads(report_path.read_text())
    report['official_density_codec_and_sampler_verified'] = True
    report['engine_validation_report'] = 'connected-engine-validation.json'
    report_path.write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
