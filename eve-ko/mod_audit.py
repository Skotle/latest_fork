from pathlib import Path
import zipfile,gzip,json,re,collections
s=next(Path('eve-ko/source').iterdir());hits=[];jh=[]
for p in (s/'mods').glob('*.jar'):
 with zipfile.ZipFile(p) as z:
  for n in z.namelist():
   if n.startswith('data/') and n.endswith('.nbt'):
    raw=z.read(n)
    try:raw=gzip.decompress(raw)
    except OSError:pass
    if b'"text"' in raw and re.search(rb'"text"\s*:\s*"[^"\n]*[a-zA-Z]',raw):hits.append((p.name,n))
   if n.startswith('data/') and n.endswith('.json'):
    raw=z.read(n)
    if re.search(rb'"text"\s*:\s*"[^"\n]*[a-zA-Z]',raw):jh.append((p.name,n))
print('mod nbt text',len(hits));print(hits[:15]);print('mod data text',len(jh));print(jh[:12])
