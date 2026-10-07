"""Real vanilla 26.3 command execution, with a disposable flat test world."""
import json
import queue
import re
import shutil
import subprocess
import threading
import time
from pathlib import Path
from bosses import BASE, BOSSES, SPELLS, DATA
from boss_visuals import make_rig

ROOT=BASE.parent
SERVER=ROOT/'.tools/boss-model-test'
JAVA=next((SERVER/'jdk').glob('*/bin/java.exe'))
WORLD='models-'+str(int(time.time()))
DEST=SERVER/WORLD/'datapacks'
DEST.mkdir(parents=True)
shutil.copy2(BASE/'output/IDA-Vanilla-26.3-Bosses-Models.zip',DEST/'IDA.zip')
(SERVER/'eula.txt').write_text('eula=true\n')
(SERVER/'server.properties').write_text('\n'.join([
 'level-name='+WORLD,'level-type=minecraft:flat','generate-structures=false',
 'generator-settings={"layers":[{"block":"minecraft:bedrock","height":1},{"block":"minecraft:stone","height":2}],"biome":"minecraft:plains"}',
 'online-mode=false','server-ip=127.0.0.1','server-port=25591','view-distance=3','simulation-distance=3',
 'spawn-protection=0','difficulty=normal','max-tick-time=-1','sync-chunk-writes=true'])+'\n')
TEST=DEST/'selftest'
FNS=TEST/'data/selftest/function';FNS.mkdir(parents=True)
(TEST/'pack.mcmeta').write_text(json.dumps({'pack':{'min_format':[121,0],'max_format':[121,0],'description':'IDA boss model validation ONLY'}}))
def fn(name,lines):(FNS/(name+'.mcfunction')).write_text('\n'.join(lines)+'\n',encoding='utf-8')
fn('target',[
 '$summon minecraft:marker ~ ~ ~6 {Tags:["ida.target","ida.aim","test.new"],data:{id:$(id)}}',
 'execute as @e[tag=test.new] store result score @s ida.sid run data get entity @s data.id',
 'tag @e[tag=test.new] remove test.new'])
fn('count_visual',[
 'scoreboard players set #count ida.tmp 0',
 '$execute as @e[tag=ida.visual,scores={ida.sid=$(id)}] run scoreboard players add #count ida.tmp 1',
 '$execute store result storage selftest:results models.$(kind) int 1 run scoreboard players get #count ida.tmp'])
fn('count_targets',[
 'scoreboard players set #count ida.tmp 0',
 '$execute as @e[tag=ida.target,scores={ida.sid=$(id)}] run scoreboard players add #count ida.tmp 1',
 '$execute store result storage selftest:results markers.$(spell) int 1 run scoreboard players get #count ida.tmp'])
fn('phases',[
 'data modify entity @s Health set value 40f',
 'function dungeons_arise:boss/core/fast with entity @s data',
 '$execute store result storage selftest:results phases.$(kind) int 1 run scoreboard players get @s ida.phase'])
lines=[]
for b in BOSSES:
 ident=b['id']
 lines += ['execute positioned 0 81 0 run function dungeons_arise:boss/admin/spawn/'+ident,
  f'execute as @e[tag=ida.boss.{ident},limit=1] at @s run function selftest:count_visual with entity @s data',
  f'execute as @e[tag=ida.boss.{ident},limit=1] at @s run function selftest:phases with entity @s data']
 # Exercise every generated pose on living models, not just check references.
 for phase in [1,2]:
  for pose in ['idle','walk','wind','recover']:
   for frame in range(4):
    lines.append(f'execute as @e[tag=ida.boss.{ident},limit=1] at @s run function dungeons_arise:boss/visual/{ident}/{phase}_{pose}_{frame} with entity @s data')
 lines += [f'loot spawn 0 82 0 loot dungeons_arise:boss/{ident}']
for skill in SPELLS:
 warn=(DATA/f'function/boss/spell/{skill}/warn.mcfunction').read_text(encoding='utf-8').splitlines()
 warn[0]='function selftest:target with entity @s data'
 fn('warn_'+skill,warn)
 lines += [f'data modify entity @e[tag=ida.boss,limit=1] data.spell set value "{skill}"',
  'kill @e[tag=ida.target]',
  f'execute as @e[tag=ida.boss,limit=1] at @s run function selftest:warn_{skill} with entity @s data',
  'execute as @e[tag=ida.boss,limit=1] run function selftest:count_targets with entity @s data',
  f'execute as @e[tag=ida.boss,limit=1] at @s run function dungeons_arise:boss/spell/{skill}/hit with entity @s data']
lines += [
 'kill @e[tag=ida.target]',
 'execute as @e[tag=ida.boss.typhon,limit=1] at @s run function dungeons_arise:boss/core/begin with entity @s data',
 'execute store result storage selftest:results cast_noai int 1 run data get entity @e[tag=ida.boss.typhon,limit=1] NoAI',
 'execute as @e[tag=ida.boss.typhon,limit=1] at @s run function dungeons_arise:boss/core/resolve with entity @s data',
 'execute store result storage selftest:results recovery_stage int 1 run scoreboard players get @e[tag=ida.boss.typhon,limit=1] ida.stage',
 'execute store result storage selftest:results recovery_ticks int 1 run scoreboard players get @e[tag=ida.boss.typhon,limit=1] ida.wind',
 'execute as @e[tag=ida.boss.typhon,limit=1] at @s run function dungeons_arise:boss/core/recover with entity @s data',
 'execute store result storage selftest:results recovered_noai int 1 run data get entity @e[tag=ida.boss.typhon,limit=1] NoAI',
 'data get entity @e[tag=ida.boss.bandit_towers,limit=1] equipment',
 'data get entity @e[tag=ida.visual,limit=1] item',
 'execute store result storage selftest:results manual_sites int 1 run execute if entity @e[tag=ida.site,tag=ida.manualsite]',
 'tp @e[tag=ida.boss] 40 81 0','function dungeons_arise:boss/contain','function dungeons_arise:boss/contain',
 'execute positioned 0 81 0 store result storage selftest:results returned_bosses int 1 run execute if entity @e[tag=ida.boss,distance=..1]',
 'execute positioned 0 81 0 store result storage selftest:results returned_visuals int 1 run execute if entity @e[tag=ida.visual,distance=..1]',
 'data get storage selftest:results']
fn('all',lines)
fn('repair',[
 'execute as @e[tag=ida.boss,limit=1] run function selftest:missing_visuals with entity @s data',
 'execute as @e[tag=ida.boss,limit=1] at @s run function dungeons_arise:boss/visual/tick with entity @s data',
 'execute as @e[tag=ida.boss,limit=1] run function selftest:count_visual with entity @s data',
 'execute store result storage selftest:results models_after_repair int 1 run execute if entity @e[tag=ida.visual]',
 'data get storage selftest:results'])
fn('missing_visuals',['$kill @e[tag=ida.visual,scores={ida.sid=$(id)}]'])
fn('clear',[
 'execute positioned 0 81 0 run function dungeons_arise:boss/admin/abort_nearby',
 'execute store result storage selftest:results models_after_abort int 1 run execute if entity @e[tag=ida.visual]',
 'execute store result storage selftest:results bosses_after_abort int 1 run execute if entity @e[tag=ida.boss]',
 'execute store result storage selftest:results targets_after_abort int 1 run execute if entity @e[tag=ida.target]',
 'data get storage selftest:results','bossbar list'])
fn('death',[
 'execute positioned 0 81 0 run function dungeons_arise:boss/admin/spawn/typhon',
 'kill @e[tag=ida.boss.typhon]'])
fn('death_result',[
 'execute store result storage selftest:results models_after_death int 1 run execute if entity @e[tag=ida.visual]',
 'scoreboard players set #victories ida.tmp 0',
 'execute as @e[tag=ida.site,scores={ida.stage=2}] if score @s ida.sid = #next ida.sid run scoreboard players add #victories ida.tmp 1',
 'execute store result storage selftest:results victories int 1 run scoreboard players get #victories ida.tmp'])

p=subprocess.Popen([str(JAVA),'-javaagent:'+str(BASE/'test-agent/test-network.jar'),'-Xms256M','-Xmx2G','-jar','server.jar','nogui'],cwd=SERVER,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
q=queue.Queue()
def pump():
 for line in p.stdout:q.put(line)
threading.Thread(target=pump,daemon=True).start()
commands=[('scoreboard players set #enabled ida.cfg 0',.5),('scoreboard players set #abandon ida.cfg 99999',.5),
 ('forceload add -32 -32 32 32',10),('fill -16 80 -16 16 80 16 minecraft:stone',1),
 ('function selftest:all',3),('data get storage selftest:results',.5),
 ('data get entity @e[tag=ida.boss.bandit_towers,limit=1] equipment',.5),
 ('data get entity @e[tag=ida.visual,limit=1] item',.5),
 ('reload',5),('function selftest:repair',2),('data get storage selftest:results',.5),
 ('function selftest:clear',2),('data get storage selftest:results',.5),('bossbar list',.5),
 ('function selftest:death',3),('function selftest:death_result',.5),('data get storage selftest:results',.5),('bossbar list',.5),('stop',1)]
logpath=BASE/'output/boss-model-smoke-console.log'
start=time.time();ready=False;i=0;nexttime=0
with logpath.open('w',encoding='utf-8') as log:
 while time.time()-start<240:
  try:line=q.get(timeout=.2)
  except queue.Empty:line=''
  if line:
   log.write(line);log.flush()
   if any(s in line for s in ['ERROR','Failed','Unknown','Done (','selftest:results','NoAI','equipment','Stopping']):print(line.rstrip(),flush=True)
   if 'Done (' in line:ready=True;nexttime=time.time()+2
  if ready and i<len(commands) and time.time()>nexttime:
   command,delay=commands[i];p.stdin.write(command+'\n');p.stdin.flush();i+=1;nexttime=time.time()+delay
  if p.poll() is not None:break
 if p.poll() is None:
  p.stdin.write('stop\n');p.stdin.flush();p.wait(timeout=30)
clean=re.sub(r'\x1b\[[0-9;]*m','',logpath.read_text(encoding='utf-8'))
errors=[l for l in clean.splitlines() if 'Unable to locate English counter names in registry Perflib' not in l and any(s in l for s in ['ERROR','Failed to load function','Unknown or incomplete command','Incorrect argument','Unknown registry'])]
assert p.returncode==0,p.returncode
assert not errors,'\n'.join(errors[:30])
assert 'Done (' in clean,'Server did not finish starting'
assert 'models_after_abort: 0' in clean and 'bosses_after_abort: 0' in clean and 'targets_after_abort: 0' in clean
assert 'cast_noai: 1' in clean and 'recovered_noai: 0' in clean
assert 'models_after_death: 0' in clean and 'victories: 1' in clean
assert 'recovery_stage: 2' in clean and 'recovery_ticks: 20' in clean
assert 'returned_bosses: 22' in clean
expected=sum(len(make_rig(b['id']).parts) for b in BOSSES)
assert f'returned_visuals: {expected}' in clean,(expected,clean[-5000:])
assert f'models_after_repair: {expected}' in clean
for b in BOSSES:
 assert f'{b["id"]}: {len(make_rig(b["id"]).parts)}' in clean,b['id']
phases=re.findall(r'phases: \{([^}]+)\}',clean)[-1]
assert len(phases.split(','))==22 and all(x.strip().endswith(': 2') for x in phases.split(','))
marker_counts={k.strip():int(v) for k,v in (x.split(':') for x in re.findall(r'markers: \{([^}]+)\}',clean)[-1].split(','))}
assert marker_counts['snipe']==6 and marker_counts['cleave']==3 and marker_counts['blast']==4 and marker_counts['web']==9 and marker_counts['tide']==1,marker_counts
assert 'minecraft:item_model' in clean and 'ida_boss:hidden' in clean
report={'engine':'Official vanilla Minecraft Java 26.3','world':WORLD,'bosses':22,'model_parts':expected,
 'pose_functions_executed':22*32,'spell_functions_executed':20,'cast_pause_and_recovery':True,
 'arena_return':True,'reload_and_missing_visual_repair':True,'abort_cleanup':True,'death_cleanup':True,
 'phase_two_count':22,'pattern_marker_counts':marker_counts,'command_errors':0,
 'network_disabled_for_local_test_only':True,
 'limitations':['No connected client: in-game render, armor visibility, player hitboxes, combat damage and multiplayer balance require a playtest.']}
(BASE/'output/boss-model-validation-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
