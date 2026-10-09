"""Package only artifacts that match the successful engine validation."""
import json, zipfile
from build import OUT, BASE, sha, js

engine=json.loads((OUT/'engine-validation.json').read_text(encoding='utf-8'))
assert engine['command_errors']==0
assert engine['datapack_sha256']==sha(OUT/'Nox-Standalone-Datapack-26.3.zip')
worldgen=json.loads((OUT/'worldgen-validation.json').read_text(encoding='utf-8'))
assert worldgen['command_errors']==0 and worldgen['natural_sites']>=1
assert worldgen['datapack_sha256']==sha(OUT/'Nox-Standalone-Datapack-26.3.zip')
crworld=json.loads((OUT/'Cristiano-dummy-validation.json').read_text(encoding='utf-8'))
assert crworld['command_only'] and not crworld['natural_placement']
assert crworld['datapack_sha256']==sha(OUT/'Nox-Standalone-Datapack-26.3.zip')
players=json.loads((OUT/'Cristiano-player-validation.json').read_text(encoding='utf-8'))
assert players['all_six_skills_seen_in_live_tick_loop'] and players['player_inventory_and_damage_tested']
assert players['datapack_sha256']==sha(OUT/'Nox-Standalone-Datapack-26.3.zip')
for report in ['Frost-player-validation.json','Frost-worldgen-validation.json','Frost-native-piercing-validation.json']:
 r=json.loads((OUT/report).read_text(encoding='utf-8'))
 assert r['datapack_sha256']==sha(OUT/'Nox-Standalone-Datapack-26.3.zip')
paths=[OUT/'Nox-Standalone-Datapack-26.3.zip',OUT/'Integrated-Resources-with-Nox-26.3.zip',
       BASE/'README.ko.md',OUT/'Nox-Preview.png',OUT/'Nox-Motion-Preview.gif',OUT/'static-validation.json',OUT/'engine-validation.json',OUT/'worldgen-validation.json',OUT/'timing-profile.json',OUT/'challenge-guide.json',OUT/'Cristiano-guide.json',OUT/'Cristiano-dummy-validation.json',OUT/'Cristiano-Bernabeu-Preview.png',OUT/'Cristiano-Model-Preview.png',OUT/'Cristiano-Motion-Preview.gif',OUT/'Cristiano-animation-guide.json',OUT/'Cristiano-photo-references.json']
paths += [OUT/'Cristiano-player-validation.json',OUT/'Cristiano-RealMadrid-Preview.png',BASE/'art/head-generation.txt',BASE/'design/frost_warden.ko.md',OUT/'Frost-guide.json',OUT/'Frost-player-validation.json',OUT/'Frost-worldgen-validation.json',OUT/'Frost-native-piercing-validation.json']
js(OUT/'release-hashes.json',{'sha256':{p.name:sha(p) for p in paths},'resourcepack_sha1':__import__('hashlib').sha1((OUT/'Integrated-Resources-with-Nox-26.3.zip').read_bytes()).hexdigest()})
paths.append(OUT/'release-hashes.json')
with zipfile.ZipFile(OUT/'Nox-Boss-Bundle-26.3-v22-Frost-Fury.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in paths:z.write(p,p.name)
print('Release bundle:',OUT/'Nox-Boss-Bundle-26.3-v22-Frost-Fury.zip')
