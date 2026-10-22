from pathlib import Path
import json,zipfile,collections,re
s=next(Path('eve-ko/source').iterdir())
fs=list((s/'config/openloader/data').rglob('*.mcfunction'))
print('functions',len(fs))
for p in fs:
 t=p.read_text('utf-8')
 if any(x in t for x in ['tellraw','title ','CustomName','Lore','pages:']):
  print(str(p.relative_to(s)),t[:1400])
  if 'spawn' not in p.name: break
print('json counts',len(list((s/'config/openloader/data').rglob('*.json'))))
for p in (s/'config/openloader/resources').rglob('en_us.json'):
 d=json.loads(p.read_text('utf-8-sig'));print(str(p.relative_to(s)),len(d))
