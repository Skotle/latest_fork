import csv, hashlib, json, re, subprocess, zipfile
from pathlib import Path

B=Path(__file__).resolve().parent
O=B/'instance-overlay'
source=Path(r'C:/Users/user/curseforge/minecraft/Instances/Create New World  A Locked Progression Experience.zip')
report=json.loads((B/'coverage.json').read_text('utf-8'))
checks=[]
for p in sorted(O.rglob('*.json')):
    json.loads(p.read_text('utf-8'));checks.append({'path':p.relative_to(O).as_posix(),'check':'JSON parse','passed':True})
for p in sorted(O.rglob('*.js')):
    result=subprocess.run(['node','--check',str(p)],capture_output=True,text=True,encoding='utf-8')
    checks.append({'path':p.relative_to(O).as_posix(),'check':'node --check','passed':result.returncode==0,'diagnostic':result.stderr.strip()})
    assert result.returncode==0,result.stderr
with zipfile.ZipFile(source) as z:
    root=z.namelist()[0].split('/')[0]+'/'
    with zipfile.ZipFile(B/'CNW-Original-Files-4.0.12.zip','w',zipfile.ZIP_DEFLATED) as backup:
        for p in sorted(O.rglob('*')):
            if not p.is_file():continue
            r=p.relative_to(O).as_posix()
            if root+r in z.namelist():backup.writestr(r,z.read(root+r))
    original=z.read(root+'config/ftbquests/quests/lang/en_us.snbt').decode('utf-8-sig')
    patched=(O/'config/ftbquests/quests/lang/ko_kr.snbt').read_text('utf-8')
    keys=lambda t:re.findall(r'^\s*([\w.]+):',t,re.M)
    assert keys(original)==keys(patched)
    checks.append({'check':'FTB quest language keys preserved','passed':True,'keys':len(keys(patched))})

with (B/'translations.tsv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.writer(f,delimiter='\t');writer.writerow(['English','한국어'])
    memory=json.loads((B/'translation-memory.json').read_text('utf-8'))
    overrides=json.loads((B/'manual-overrides.json').read_text('utf-8'));memory.update(overrides)
    for en,ko in sorted(memory.items()):writer.writerow([en,ko])

# Collapse duplicate file entries caused by merging custom and mod language keys.
merged={x['path']:x.copy() for x in report['files']}
for r,d in merged.items():
    if r.endswith('.json'):d['entries']=len(json.loads((O/r).read_text('utf-8')))
    if r.endswith('quests/lang/ko_kr.snbt'):d['language_keys']=len(keys(patched))
report['files']=list(merged.values())
report['total_output_files']=len(merged)
report['priority_mod_missing_keys_included']=sum(x['missing_keys'] for x in report['mods'] if x['included'])
report['remaining_mod_missing_keys']=sum(x['missing_keys'] for x in report['mods'] if not x['included'])
(B/'coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

with zipfile.ZipFile(B/'CNW-Korean-Full-4.0.12.zip','w',zipfile.ZIP_DEFLATED) as pack:
    for p in sorted(O.rglob('*')):
        if p.is_file():pack.write(p,p.relative_to(O).as_posix())
    for name in ['README.ko.md','coverage.json']:pack.write(B/name,name)

for name in ['CNW-Korean-Full-4.0.12.zip','CNW-Korean-Resources-4.0.12.zip','CNW-Original-Files-4.0.12.zip']:
    with zipfile.ZipFile(B/name) as z:
        assert z.testzip() is None
        checks.append({'path':name,'check':'ZIP CRC and relative entry paths','passed':True,'entries':len(z.namelist())})
        assert all(not n.startswith('/') and '..' not in Path(n).parts for n in z.namelist())
validation={'all_static_checks_passed':all(x['passed'] for x in checks),'in_game_tested':False,'snbt_validation':'Language keys, quoted strings, protected tokens and non-string structure compared with source; game parser not executed','checks':checks}
(B/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with zipfile.ZipFile(B/'CNW-Korean-Full-4.0.12.zip','a',zipfile.ZIP_DEFLATED) as pack:pack.write(B/'validation.json','validation.json')
with (B/'SHA256SUMS.txt').open('w',encoding='utf-8') as f:
    for p in sorted(B.glob('*.zip')):f.write(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n')
print(json.dumps({'files':len(merged),'quest_keys':len(keys(patched)),'priority_mod_keys':report['priority_mod_missing_keys_included'],'checks_passed':len(checks),'archives':[{ 'name':p.name,'bytes':p.stat().st_size} for p in B.glob('*.zip')]},indent=2))
