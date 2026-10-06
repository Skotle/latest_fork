import pathlib, subprocess, shutil, time, threading, queue, json, re
from bosses import BOSSES, SPELLS
BASE=pathlib.Path(__file__).resolve().parent;ROOT=BASE.parent;SERVER=ROOT/'.tools/ida263-smoke'
world='boss-test-'+str(int(time.time()));dest=SERVER/world/'datapacks';dest.mkdir(parents=True)
props=(SERVER/'server.properties').read_text();(SERVER/'server.properties').write_text(re.sub(r'(?m)^level-name=.*$','level-name='+world,props))
shutil.copy2(BASE/'output/IDA-Vanilla-26.3-Bosses.zip',dest/'IDA.zip')
test=dest/'selftest';(test/'data/selftest/function').mkdir(parents=True)
(test/'pack.mcmeta').write_text(json.dumps({'pack':{'min_format':[121,0],'max_format':[121,0],'description':'Boss validation'}}))
lines=[]
for b in BOSSES:
 lines += ['execute positioned 0 81 0 run function dungeons_arise:boss/admin/spawn/'+b['id']]
 lines += [f'execute as @e[tag=ida.boss.{b["id"]},limit=1] store result storage selftest:results health.{b["id"]} int 1 run data get entity @s Health',f'data modify entity @e[tag=ida.boss.{b["id"]},limit=1] Health set value 40f',f'execute as @e[tag=ida.boss.{b["id"]},limit=1] at @s run function dungeons_arise:boss/core/fast with entity @s data',f'execute store result storage selftest:results phase.{b["id"]} int 1 run scoreboard players get @e[tag=ida.boss.{b["id"]},limit=1] ida.phase']
 lines += [f'execute as @e[tag=ida.boss.{b["id"]},limit=1] store result storage selftest:results period.{b["id"]} int 1 run data get entity @s data.period']
 lines += ['loot spawn 0 82 0 loot dungeons_arise:boss/'+b['id']]
fixture=['$summon minecraft:marker ~ ~ ~ {Tags:["ida.target","test.target"],data:{id:$(id)}}','execute as @e[tag=test.target] store result score @s ida.sid run data get entity @s data.id','tag @e[tag=test.target] remove test.target']
(test/'data/selftest/function/target.mcfunction').write_text('\n'.join(fixture)+'\n',encoding='utf-8')
for skill in SPELLS:
 lines += [f'execute as @e[tag=ida.boss,limit=1] at @s run function dungeons_arise:boss/spell/{skill}/warn with entity @s data','execute as @e[tag=ida.boss,limit=1] at @s run function selftest:target with entity @s data',f'execute as @e[tag=ida.boss,limit=1] at @s run function dungeons_arise:boss/spell/{skill}/hit with entity @s data','kill @e[tag=ida.target]']
lines += [
 'execute as @e[tag=ida.boss.desert_hall,limit=1] at @s run function dungeons_arise:boss/core/begin with entity @s data',
 'execute store result storage selftest:results sunfire_warning_ticks int 1 run scoreboard players get @e[tag=ida.boss.desert_hall,limit=1] ida.wind',
 'execute as @e[tag=ida.boss.typhon,limit=1] at @s run function dungeons_arise:boss/core/begin with entity @s data',
 'execute store result storage selftest:results normal_warning_ticks int 1 run scoreboard players get @e[tag=ida.boss.typhon,limit=1] ida.wind',
 'execute store result storage selftest:results adds_before_return int 1 run execute if entity @e[tag=ida.add]',
 'tp @e[tag=ida.boss] 40 81 0','tp @e[tag=ida.add] 40 81 0',
 'function dungeons_arise:boss/contain',
 'execute positioned 0 81 0 store result storage selftest:results returned_bosses int 1 run execute if entity @e[tag=ida.boss,distance=..1]',
 'execute positioned 0 81 0 store result storage selftest:results returned_adds int 1 run execute if entity @e[tag=ida.add,distance=..1]']
lines += ['execute as @e[tag=ida.boss,limit=1] run data get entity @s Health','execute as @e[tag=ida.boss,limit=1] run data get entity @s attributes','execute as @e[type=item,limit=1] run data get entity @s Item','execute store result storage selftest:results manual_sites int 1 run execute if entity @e[tag=ida.site,tag=ida.manualsite]','execute store result storage selftest:results bosses int 1 run execute if entity @e[tag=ida.boss]','data get storage selftest:results','kill @e[tag=ida.boss]']
(test/'data/selftest/function/all.mcfunction').write_text('\n'.join(lines)+'\n',encoding='utf-8')
p=subprocess.Popen([str(ROOT/'.tools/jdk25/jdk-25.0.4.1+1/bin/java.exe'),'-javaagent:'+str(BASE/'test-agent/test-network.jar'),'-Xms256M','-Xmx3G','-jar','paper.jar','--nogui'],cwd=SERVER,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
q=queue.Queue()
def pump():
 for line in p.stdout:q.put(line)
threading.Thread(target=pump,daemon=True).start()
commands=['datapack list enabled','scoreboard players set #abandon ida.cfg 99999','scoreboard players set #enabled ida.cfg 0','forceload add -32 -32 32 32','fill -16 80 -16 16 80 16 minecraft:stone','function selftest:all','execute store result storage selftest:results cleared int 1 run execute if entity @e[tag=ida.site,scores={ida.stage=2}]','data get storage selftest:results','bossbar list','stop']
start=time.time();ready=False;i=0;nexttime=0
with (BASE/'output/boss-smoke-console.log').open('w',encoding='utf-8') as out:
 while time.time()-start<240:
  try:line=q.get(timeout=.2)
  except queue.Empty:line=''
  if line:
   out.write(line);out.flush()
   if any(s in line for s in ['ERROR','Failed','Unknown','Done (','selftest','enabled data','boss bars','has the following']):print(line.rstrip(),flush=True)
   if 'Done (' in line:ready=True;nexttime=time.time()+2
  if ready and i<len(commands) and time.time()>nexttime:
   p.stdin.write(commands[i]+'\n');p.stdin.flush();print('COMMAND',commands[i],flush=True);i+=1;nexttime=time.time()+(20 if i==4 else 5 if i==6 else 2)
  if p.poll() is not None:break
 if p.poll() is None:p.stdin.write('stop\n');p.stdin.flush();p.wait(timeout=60)
print('EXIT',p.returncode,'WORLD',world)
