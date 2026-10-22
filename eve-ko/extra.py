import zipfile,re
from pathlib import Path
s=next(Path('eve-ko/source').iterdir())
for p in (s/'mods').glob('*.jar'):
 with zipfile.ZipFile(p) as z:
  names=[n for n in z.namelist() if re.search(r'(en_us|ko_kr|en_US|ko_KR)',n) and not n.endswith('/')]
  extra=[n for n in names if not re.fullmatch('assets/[^/]+/lang/(en_us|ko_kr).json',n)]
  if extra:print(p.name,'\n'+'\n'.join(extra)[:6000])
print('FUNCTION EXAMPLES')
i=0
for p in (s/'config/openloader/data').rglob('*.mcfunction'):
 for line in p.read_text('utf-8').splitlines():
  if not line.startswith('#') and any(x in line for x in ['tellraw','title ','CustomName','Lore','pages:']):
   print(line[:1500]);i+=1
   if i>16:break
 if i>16:break
