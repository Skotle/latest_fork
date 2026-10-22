from pathlib import Path
import zipfile,json,re
b=Path(__file__).parent
s=next((b/'source').iterdir())
rows=[]
for p in sorted((s/'mods').glob('*.jar')):
 with zipfile.ZipFile(p) as z:
  ns=set(z.namelist())
  for n in sorted(ns):
   if re.fullmatch(r'assets/[^/]+/lang/en_us.json',n):
    try:
     en=json.loads(z.read(n)); ko=json.loads(z.read(n.replace('en_us','ko_kr'))) if n.replace('en_us','ko_kr') in ns else {}
     rows.append({'jar':p.name,'path':n,'en':len(en),'ko':len(ko),'missing':len(set(en)-set(ko))})
    except Exception as e: print(n,str(e))
  books=[n for n in ns if '/patchouli_books/' in n and '/en_us/' in n and n.endswith('.json')]
  if books:print('BOOK',p.name,len(books))
print(json.dumps(rows,indent=2))
(b/'audit.json').write_text(json.dumps(rows,indent=2))
print('CUSTOM')
for d in ['patchouli_books','resourcepacks','config/openloader']:
 for p in (s/d).rglob('*'):
  if p.is_file() and p.suffix not in ['.nbt','.png','.ogg']:print(p.relative_to(s))
