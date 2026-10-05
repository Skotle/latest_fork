"""Repair remaining saved-state fields without repeating palette conversion."""
import gzip,re
from build import BASE,OUT,clean_nbt,stats
from nbt_io import read,write
count=0
for f in OUT.rglob('*.nbt'):
 raw=gzip.decompress(f.read_bytes())
 if not any(v in raw for v in [b'clayworks:base',b'final_state',b'decorated_pot',b'attributes',b'Attributes']):continue
 name,root=read(raw);clean_nbt(root.value)
 f.write_bytes(gzip.compress(write(name,root),mtime=0));count+=1
 if count%100==0:print('repaired',count,flush=True)
print('NBT saved-state repairs:',count,dict(stats),flush=True)
