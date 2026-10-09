"""Verify that preserved experimental assets have no natural placement or survival trigger."""
import json,zipfile
from build import OUT,js,sha
p=OUT/'Nox-Standalone-Datapack-26.3.zip'
with zipfile.ZipFile(p) as z:
 names=z.namelist()
 assert 'data/desert_ball/structure/bernabeu.nbt' in names
 assert 'data/desert_ball/worldgen/structure_set/stadiums.json' not in names
 for n in names:
  if '/worldgen/structure_set/' in n and n.endswith('.json'):
   assert 'desert_ball:bernabeu' not in z.read(n).decode(),n
 tick=z.read('data/desert_ball/function/tick.mcfunction').decode()
 start=z.read('data/desert_ball/function/start.mcfunction').decode()
 setup=z.read('data/desert_ball/function/site/setup.mcfunction').decode()
 assert 'run function desert_ball:start' not in tick
 assert 'function desert_ball:begin' not in start
 assert 'summon minecraft:interaction' not in setup
 assert 'kill @e[tag=db.start]' in tick
 assert 'function desert_ball:begin' in z.read('data/desert_ball/function/admin/summon.mcfunction').decode()
js(OUT/'Cristiano-dummy-validation.json',{'command_only':True,'natural_placement':False,
 'survival_start_disabled':True,'old_start_entities_removed':True,'manual_arena_and_boss_preserved':True,
 'datapack_sha256':sha(p)})
print('Cristiano command-only dummy checks passed.')
