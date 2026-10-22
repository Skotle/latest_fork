from pathlib import Path
import json,zipfile,re,collections
s=next(Path('eve-ko/source').iterdir()); out={}
for p in (s/'mods').glob('*.jar'):
 with zipfile.ZipFile(p) as z:
  for n in z.namelist():
   if n.endswith('/en_us.json') and '/lang/' in n:
    try:d=json.loads(z.read(n))
    except:continue
    for k,v in d.items():
     if not isinstance(v,str):print('NONSTRING',n,k,type(v))
print('book txt');p=s/'mods/citadel-2.3.4-1.19.4.jar'
with zipfile.ZipFile(p) as z:print(z.read('assets/citadel/book/citadel_book/en_us/root.txt').decode()[:3000])
print('NBT',len(list((s/'config/openloader').rglob('*.nbt'))))
