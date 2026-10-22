from pathlib import Path
import difflib
src=Path('eve-ko/verify_package.py').read_text('utf-8');exec(src.split('for p in O.rglob')[0])
for rel in ['second.mcfunction','boss/aerwhale_king/hint.mcfunction','world/bed_spawn_point.mcfunction']:
 p=O/'config/openloader/data/Explorer\'s Eve Core/data/explorers_eve/functions'/rel
 a=cmdshape((S/p.relative_to(O)).read_text('utf-8-sig'));b=cmdshape(p.read_text('utf-8'))
 for x in difflib.unified_diff(a.splitlines(),b.splitlines()):
  if x.startswith(('+','-')):print(x)
