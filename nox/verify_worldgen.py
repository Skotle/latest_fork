"""Verify native random underground generation in a fresh normal Overworld."""
import json, queue, re, shutil, subprocess, threading, time
from build import BASE, ROOT, OUT, js, sha

SERVER=BASE/'worldgen-test';SERVER.mkdir(exist_ok=True)
WORLD='underground-'+str(int(time.time()));dest=SERVER/WORLD/'datapacks';dest.mkdir(parents=True)
shutil.copy2(OUT/'Nox-Standalone-Datapack-26.3.zip',dest/'Nox.zip')
shutil.copy2(ROOT/'.tools/ida263-smoke/cache/mojang_26.3.jar',SERVER/'server.jar')
(SERVER/'eula.txt').write_text('eula=true\n')
(SERVER/'server.properties').write_text('\n'.join(['level-name='+WORLD,'level-type=minecraft:normal','level-seed=73102631',
 'generate-structures=true','online-mode=false','server-ip=127.0.0.1','server-port=25597','view-distance=3','simulation-distance=3',
 'max-tick-time=-1','sync-chunk-writes=true'])+'\n')
test=dest/'selftest';js(test/'pack.mcmeta',{'pack':{'min_format':[121,0],'max_format':[121,0],'description':'Nox natural generation test'}})
fns=test/'data/selftest/function';fns.mkdir(parents=True)
checks=[
 'execute store result storage selftest:worldgen seeds int 1 run execute if entity @e[tag=nox.seed]',
 'execute as @e[tag=nox.seed,limit=1] store result storage selftest:worldgen floor_y int 1 run data get entity @s Pos[1]',
 'execute at @e[tag=nox.seed,limit=1] store result storage selftest:worldgen floor_block int 1 run execute if block ~ ~-1 ~ minecraft:deepslate_tiles',
 'execute at @e[tag=nox.seed,limit=1] store result storage selftest:worldgen roof_block int 1 run execute if block ~ ~17 ~ minecraft:chiseled_deepslate',
 'execute at @e[tag=nox.seed,limit=1] store result storage selftest:worldgen inside_air int 1 run execute if block ~ ~5 ~ minecraft:air',
 'execute as @e[tag=nox.seed] at @s run function eclipse_nox:site/init',
 'execute store result storage selftest:worldgen anchors int 1 run execute if entity @e[tag=nox.anchor]',
 'execute store result storage selftest:worldgen bells int 1 run execute if entity @e[tag=nox.bell,type=minecraft:interaction]',
 'execute at @e[tag=nox.anchor,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["test.origin"]}',
 # Verify a second independent site via native template placement; no player needed.
 'execute at @e[tag=test.origin,limit=1] run place template eclipse_nox:observatory ~120 ~-2 ~-34',
 'execute as @e[tag=nox.seed] at @s run function eclipse_nox:site/init',
 'execute store result storage selftest:worldgen multiple_sites int 1 run execute if entity @e[tag=nox.anchor]',
 'execute at @e[tag=test.origin,limit=1] positioned ~154 ~ ~ run function eclipse_nox:site/select',
 'execute store result storage selftest:worldgen idle_selection_clear int 1 run execute unless entity @e[tag=nox.current]',
 'kill @e[tag=test.origin]']
(fns/'check.mcfunction').write_text('\n'.join(checks)+'\n',encoding='utf-8')
java=ROOT/'.tools/jdk25/jdk-25.0.4.1+1/bin/java.exe'
p=subprocess.Popen([str(java),'-javaagent:'+str(ROOT/'ida26/test-agent/test-network.jar'),'-Xms256M','-Xmx3G','-jar','server.jar','nogui'],cwd=SERVER,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
q=queue.Queue()
def pump():
 for line in p.stdout:q.put(line)
threading.Thread(target=pump,daemon=True).start()
def send(s):p.stdin.write(s+'\n');p.stdin.flush()
start=time.time();stage=0;nexttime=0;located=None;logpath=OUT/'worldgen-console.log'
with logpath.open('w',encoding='utf-8') as log:
 while time.time()-start<300:
  try:line=q.get(timeout=.2)
  except queue.Empty:line=''
  if line:
   log.write(line);log.flush()
   if any(s in line for s in ['ERROR','Failed','Done (','nearest','selftest:worldgen','Stopping']):print(line.rstrip(),flush=True)
   if 'Done (' in line and stage==0:send('locate structure eclipse_nox:observatory');stage=1
   if 'Could not find a structure' in line and stage==1:send('stop');stage=5
   found=re.search(r'nearest eclipse_nox:observatory is at \[(-?\d+), ([^,]+), (-?\d+)\]',line)
   if found and stage==1:
    x,z=int(found[1]),int(found[3]);located={'x':x,'z':z}
    # Loaded area includes the native site and the additional site activation test.
    send(f'forceload add {x-64} {z-64} {x+208} {z+64}');stage=2;nexttime=time.time()+40
  if stage==2 and time.time()>nexttime:send('function selftest:check');stage=3;nexttime=time.time()+3
  if stage==3 and time.time()>nexttime:send('data get storage selftest:worldgen');stage=4;nexttime=time.time()+1
  if stage==4 and time.time()>nexttime:send('stop');stage=5
  if p.poll() is not None:break
 if p.poll() is None:send('stop');p.wait(timeout=30)
clean=logpath.read_text(encoding='utf-8')
assert located,'Natural structure was not locatable'
errors=[l for l in clean.splitlines() if 'Unable to locate English counter names in registry Perflib' not in l and any(s in l for s in ['ERROR','Failed to load function','Unknown or incomplete','Incorrect argument'])]
assert not errors,'\n'.join(errors[:20])
match=re.search(r'floor_y: (-?\d+)',clean);assert match,clean[-3000:]
y=int(match[1]);assert -45<=y<=-21,y
for k in ['floor_block','roof_block','inside_air','idle_selection_clear']:assert re.search(r'\b'+k+r': 1\b',clean),k
seeds=int(re.search(r'\bseeds: (\d+)',clean)[1]);anchors=int(re.search(r'\banchors: (\d+)',clean)[1]);multi=int(re.search(r'\bmultiple_sites: (\d+)',clean)[1])
assert seeds>=1 and anchors>=1 and multi>anchors,(seeds,anchors,multi)
js(OUT/'worldgen-validation.json',{'engine':'Official vanilla Minecraft Java 26.3','seed':73102631,'world':WORLD,'located':located,'natural_sites':seeds,'floor_y':y,'underground_shell_and_air_verified':True,'multiple_sites':multi,'idle_site_selection_cleared':True,'command_errors':0,'datapack_sha256':sha(OUT/'Nox-Standalone-Datapack-26.3.zip'),'limitations':['Natural generation tested on one normal-world seed; no player discovery playtest.']})
print('Natural underground worldgen passed.',flush=True)
