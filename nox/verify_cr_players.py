"""Test all six skills using an in-process vanilla ServerPlayer, no network client."""
import json,queue,re,shutil,subprocess,threading,time,zipfile
from pathlib import Path
from build import BASE,ROOT,OUT,js,sha
SERVER=BASE/'player-test';SERVER.mkdir(exist_ok=True)
WORLD='players-'+str(int(time.time()));dest=SERVER/WORLD/'datapacks';dest.mkdir(parents=True)
shutil.copy2(OUT/'Nox-Standalone-Datapack-26.3.zip',dest/'Nox.zip')
probe=BASE/'player-probe';java=ROOT/'.tools/jdk25/jdk-25.0.4.1+1/bin/java.exe'
javac=java.with_name('javac.exe')
serverjar=BASE/'engine-test/versions/26.3/server-26.3.jar'
libs=list((BASE/'engine-test/libraries').rglob('*.jar'))
network=ROOT/'ida26/test-agent/test-network.jar';asm=ROOT/'ida26/test-agent/asm.jar'
classpath=';'.join(map(str,[serverjar,network,asm,*libs]))
subprocess.run([str(javac),'-cp',classpath,*map(str,probe.glob('*.java'))],check=True)
agent=probe/'player-probe.jar'
with zipfile.ZipFile(agent,'w') as z:
 z.writestr('META-INF/MANIFEST.MF','Manifest-Version: 1.0\nPremain-Class: TestPlayerAgent\n\n')
 for p in probe.glob('*.class'):z.write(p,p.name)
 with zipfile.ZipFile(network) as n:
  for p in n.namelist():
   if p.endswith('.class'):z.writestr(p,n.read(p))
(SERVER/'eula.txt').write_text('eula=true\n')
(SERVER/'server.properties').write_text('\n'.join(['level-name='+WORLD,'level-type=minecraft:flat','generate-structures=false',
 'generator-settings={"layers":[{"block":"minecraft:bedrock","height":1},{"block":"minecraft:stone","height":2}],"biome":"minecraft:plains"}',
 'online-mode=false','server-ip=127.0.0.1','server-port=25595','view-distance=3','simulation-distance=3','spawn-protection=0','difficulty=normal','max-tick-time=-1'])+'\n')
test=dest/'selftest';js(test/'pack.mcmeta',{'pack':{'min_format':[121,0],'max_format':[121,0],'description':'Actual vanilla ServerPlayer probe'}})
fns=test/'data/selftest/function';fns.mkdir(parents=True)
def fn(name,lines):(fns/(name+'.mcfunction')).write_text('\n'.join(lines)+'\n',encoding='utf-8')
def save(key,cmd):return 'execute store result storage selftest:results '+key+' int 1 run '+cmd
fn('setup',['forceload add 96 -48 160 48','execute positioned 128 81 0 run function desert_ball:admin/install',
 'execute positioned 128 81 0 run function desert_ball:admin/summon',
 save('member','execute if entity @a[tag=db.member]'),save('health','data get entity @e[tag=db.boss,limit=1] Health'),
 'execute as @e[tag=db.anchor,tag=db.current] at @s run function desert_ball:fight/tick',save('active','execute if entity @a[tag=db.active]'),
 'scoreboard players set #next db.next 9999','scoreboard players set #time db.time 100',
 'clear @a[tag=probe.player]','item replace entity @a[tag=probe.player,limit=1] weapon.mainhand with minecraft:diamond[minecraft:custom_data={keep:73}] 3',
 'execute as @a[tag=probe.player] at @s run function desert_ball:theft/attempt',
 save('debt','scoreboard players get @a[tag=probe.player,limit=1] db.debt'),
 save('remaining','data get entity @a[tag=probe.player,limit=1] Inventory[{Slot:0b}].count'),
 save('kept_components','data get entity @a[tag=probe.player,limit=1] Inventory[{Slot:0b}].components."minecraft:custom_data".keep'),
 'tag @a[tag=probe.player] add probe.attack'])
fn('attack_check',[save('actual_hp','data get entity @e[tag=db.boss,limit=1] Health 100'),save('attack_refund','scoreboard players get @a[tag=probe.player,limit=1] db.debt'),
 save('refund_drop_count','data get entity @e[tag=db.refund,limit=1] Item.count'),
 save('refund_components','data get entity @e[tag=db.refund,limit=1] Item.components."minecraft:custom_data".keep'),
 save('refund_owner','data get entity @e[tag=db.refund,limit=1] Owner[0]'),
 save('refund_vault_cleared','execute unless data storage desert_ball:vault accounts.p1'),
 save('boss_hurt','execute unless entity @e[tag=db.boss,nbt={Health:750f}]'),
 'scoreboard players set #safe db.safe 0','scoreboard players set #cast db.cast 40','scoreboard players set #skill db.skill 2',
 'execute store result score #origin db.tmp run data get entity @e[tag=db.anchor,tag=db.current,limit=1] Pos[1] 100',
 'execute as @e[tag=db.anchor,tag=db.current,limit=1] at @s run function desert_ball:skills/casting',
 'execute store result score #y db.tmp run data get entity @e[tag=db.anchor,tag=db.current,limit=1] Pos[1] 100',
 'scoreboard players operation #y db.tmp -= #origin db.tmp',save('anchor_not_hidden','scoreboard players get #y db.tmp'),
 'execute store result score #y db.tmp run data get entity @e[tag=db.boss,limit=1] Pos[1] 100',
 'scoreboard players operation #y db.tmp -= #origin db.tmp',save('boss_hidden','scoreboard players get #y db.tmp'),
 'function desert_ball:skills/ambush_warn','function desert_ball:skills/resolve',
 'scoreboard players set #cast db.cast 0',
 'execute at @a[tag=probe.player,limit=1] store result storage selftest:results rear_ambush int 1 run execute if entity @e[tag=db.boss,distance=..4]',
 save('chest_counter','execute if entity @e[tag=db.core]'),
 'damage @e[tag=db.core,limit=1] 2 minecraft:generic','function desert_ball:skills/core_tick'])
fn('noshow',['scoreboard players set #safe db.safe 0','scoreboard players set #cast db.cast 40','scoreboard players set #skill db.skill 3',
 'function desert_ball:skills/noshow','function desert_ball:skills/noshow',save('decoys_bounded','execute if entity @e[tag=db.decoy]'),
 'function desert_ball:visual/tick',
 'execute store result score #ballscale db.tmp run data get entity @e[tag=db.carried_ball,limit=1] transformation.scale[0] 100',
 save('real_ball_visible','execute if score #ballscale db.tmp matches 100..120'),
 'function desert_ball:skills/resolve',save('decoys_expired','execute unless entity @e[tag=db.decoy]'),
 'scoreboard players set #cast db.cast 0',
 'execute store result storage selftest:results before_hit int 1 run data get entity @a[tag=probe.player,limit=1] Health 10'])
fn('projectile',['scoreboard players set #skill db.skill 1','function desert_ball:skills/shoot',
 'execute as @e[tag=db.shot] at @a[tag=probe.player,limit=1] run tp @s ~ ~ ~ 0 0',
 'execute as @e[tag=db.shot] at @s run function desert_ball:shot/tick',
 save('after_hit','data get entity @a[tag=probe.player,limit=1] Health 10'),
 'function desert_ball:abort'])
fn('natural',['scoreboard objectives add probe.seen dummy',
 *[f'scoreboard players set #{i} probe.seen 0' for i in range(1,7)],
 'execute positioned 128 81 0 run function desert_ball:admin/summon'])
fn('tick',[f'execute if score #state db.state matches 1 if score #skill db.skill matches {i} if score #cast db.cast matches 1.. run scoreboard players set #{i} probe.seen 1' for i in range(1,7)])
js(test/'data/minecraft/tags/function/tick.json',{'values':['selftest:tick']})
fn('results',[*[save('seen_'+str(i),f'scoreboard players get #{i} probe.seen') for i in range(1,7)],
 'data get storage selftest:results','function desert_ball:abort'])
p=subprocess.Popen([str(java),'-javaagent:'+str(agent),'-Xms256M','-Xmx2G','-cp',classpath+';'+str(agent),'net.minecraft.server.Main','nogui'],
 cwd=SERVER,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
q=queue.Queue()
def pump():
 for line in p.stdout:q.put(line)
threading.Thread(target=pump,daemon=True).start()
commands=[('function selftest:setup',2),('function selftest:attack_check',2),('function selftest:noshow',2),
 ('function selftest:projectile',2),('function selftest:natural',25),('function selftest:results',1),('data get storage selftest:results',1),('stop',0)]
log=[];start=time.time();ready=False;nexttime=0;index=0
while time.time()-start<180:
 try:
  line=q.get(timeout=.1);log.append(line)
  if 'ERROR' in line or 'PROBE_' in line or 'selftest:results has' in line:print(line.strip(),flush=True)
  if 'PLAYER_PROBE_READY' in line:ready=True;nexttime=time.time()+4
 except queue.Empty:pass
 if ready and index<len(commands) and time.time()>=nexttime:
  cmd,delay=commands[index];p.stdin.write(cmd+'\n');p.stdin.flush();index+=1;nexttime=time.time()+delay
 if p.poll() is not None:break
else:p.kill();raise RuntimeError('Player probe timed out')
clean=''.join(log);(OUT/'Cristiano-player-console.log').write_text(clean,encoding='utf-8')
assert p.returncode==0 and ready,clean[-6000:]
expected={'member':1,'health':750,'active':1,'debt':1,'remaining':2,'kept_components':73,
 'attack_refund':0,'refund_drop_count':1,'refund_components':73,'refund_owner':305419896,'refund_vault_cleared':1,'boss_hurt':1,'anchor_not_hidden':0,'boss_hidden':-500,'rear_ambush':1,
 'chest_counter':1,'decoys_bounded':12,'real_ball_visible':1,'decoys_expired':1,**{'seen_'+str(i):1 for i in range(1,7)}}
for k,v in expected.items():assert re.search(r'\b'+k+r': '+str(v)+r'\b',clean),(k,v,clean[-6000:])
before=int(re.search(r'\bbefore_hit: (\d+)',clean)[1]);after=int(re.search(r'\bafter_hit: (\d+)',clean)[1]);assert before-after==30,(before,after)
js(OUT/'Cristiano-player-validation.json',{'engine':'Vanilla Java 26.3, in-process ServerPlayer',
 'assertions':expected,'ranged_damage':3,'datapack_sha256':sha(OUT/'Nox-Standalone-Datapack-26.3.zip'),
 'all_six_skills_seen_in_live_tick_loop':True,'player_inventory_and_damage_tested':True,
 'limitations':['Packet sends suppressed; no connected client or client rendering test.']})
print('Actual ServerPlayer combat probe passed.')
