"""Exercise Nox in a disposable official vanilla 26.3 world (no clients)."""
import json, queue, re, shutil, subprocess, threading, time
from pathlib import Path
from build import BASE, ROOT, OUT, DP, js, sha

SERVER=BASE/'engine-test'
SERVER.mkdir(exist_ok=True)
WORLD='nox-'+str(int(time.time()))
dest=SERVER/WORLD/'datapacks';dest.mkdir(parents=True)
shutil.copy2(OUT/'Nox-Standalone-Datapack-26.3.zip',dest/'Nox.zip')
jar=ROOT/'.tools/ida263-smoke/cache/mojang_26.3.jar'
shutil.copy2(jar,SERVER/'server.jar')
(SERVER/'eula.txt').write_text('eula=true\n')
(SERVER/'server.properties').write_text('\n'.join(['level-name='+WORLD,'level-type=minecraft:flat','generate-structures=false',
 'generator-settings={"layers":[{"block":"minecraft:bedrock","height":1},{"block":"minecraft:stone","height":2}],"biome":"minecraft:plains"}',
 'online-mode=false','server-ip=127.0.0.1','server-port=25596','view-distance=3','simulation-distance=3','spawn-protection=0','difficulty=normal','max-tick-time=-1'])+'\n')
test=dest/'selftest';js(test/'pack.mcmeta',{'pack':{'min_format':[121,0],'max_format':[121,0],'description':'Nox engine test only'}})
fns=test/'data/selftest/function';fns.mkdir(parents=True)
def fn(name,lines):(fns/(name+'.mcfunction')).write_text('\n'.join(lines)+'\n',encoding='utf-8')
def save(key,command):return 'execute store result storage selftest:results '+key+' int 1 run '+command
fn('spawn',['tag @e[tag=nox.anchor,limit=1] add nox.current','scoreboard players set #dash nx.dash 0','scoreboard players set #expose nx.expose 0',
 'scoreboard players operation #active_site nx.tmp = @e[tag=nox.current,limit=1] nx.tmp',
 'scoreboard players set #max nx.max 800','data modify storage eclipse_nox:runtime hp set value 800',
 'execute at @e[tag=nox.anchor,limit=1] run function eclipse_nox:fight/summon with storage eclipse_nox:runtime',
 save('boss_count','execute if entity @e[tag=nox.boss]'),save('health','data get entity @e[tag=nox.boss,limit=1] Health'),
 save('visuals','execute if entity @e[tag=nox.bodypart]'),
 'scoreboard players set #state nx.state 1','scoreboard players set #phase nx.phase 1',
 'scoreboard players set #cast nx.cast 0','scoreboard players set #next nx.next 1000',
 'scoreboard players set #idle nx.idle 0','scoreboard players set #grace nx.grace 99999',
 'scoreboard players set #time nx.time 0','scoreboard players set #safe nx.safe 0'])
fn('phase2',['data modify entity @e[tag=nox.boss,limit=1] Health set value 500f',
 'execute at @e[tag=nox.anchor,limit=1] run function eclipse_nox:fight/alive',
 save('phase2','scoreboard players get #phase nx.phase'),save('shield','data get entity @e[tag=nox.boss,limit=1] Invulnerable'),
 'scoreboard players set #step nx.step 0','scoreboard players set #last nx.last 0','scoreboard players set #lock nx.lock 0',
 'execute as @e[tag=nox.bell1,type=minecraft:interaction,limit=1] at @s run function eclipse_nox:puzzle/press',
 save('step1','scoreboard players get #step nx.step'),
 'execute as @e[tag=nox.bell3,type=minecraft:interaction,limit=1] at @s run function eclipse_nox:puzzle/press',
 save('step2','scoreboard players get #step nx.step'),
 'execute as @e[tag=nox.bell2,type=minecraft:interaction,limit=1] at @s run function eclipse_nox:puzzle/press',
 save('step3','scoreboard players get #step nx.step'),
 'execute at @e[tag=nox.anchor,limit=1] run function eclipse_nox:puzzle/success',
 save('unshield','data get entity @e[tag=nox.boss,limit=1] Invulnerable'),
 'data modify entity @e[tag=nox.boss,limit=1] Health set value 200f',
 'execute at @e[tag=nox.anchor,limit=1] run function eclipse_nox:fight/alive',
 save('phase3','scoreboard players get #phase nx.phase')])
lines=['summon minecraft:marker 0 81 0 {Tags:["nox.owned","nox.target"]}']
for name in ['cleave_warn','cleave_hit','ring_warn','ring_hit','echo','eclipse_begin','eclipse_tick','resolve']:
 lines.append('execute at @e[tag=nox.anchor,limit=1] run function eclipse_nox:skills/'+name)
for i in range(8):lines.append(f'execute at @e[tag=nox.anchor,limit=1] run function eclipse_nox:skills/eclipse/{i}')
lines += ['execute as @e[tag=nox.bell1,type=minecraft:interaction,limit=1] at @s run function eclipse_nox:puzzle/overload',
 save('overload','execute if entity @e[tag=nox.overload]'),
 'scoreboard players set @e[tag=nox.overload] nx.time 1',
 'summon minecraft:marker 0 81 0 {Tags:["nox.owned","nox.echo"]}',
 'scoreboard players set @e[tag=nox.echo] nx.time 1',
 'execute at @e[tag=nox.anchor,limit=1] run function eclipse_nox:hazards/tick',
 save('expired_hazards','execute if entity @e[tag=nox.echo]'),
 'execute at @e[tag=nox.anchor,limit=1] run function eclipse_nox:admin/abort',
 save('after_abort','execute if entity @e[tag=nox.boss]'),
 save('after_abort_parts','execute if entity @e[tag=nox.bodypart]'),
 save('state_abort','scoreboard players get #state nx.state'),
 save('preserved_bells','execute if entity @e[tag=nox.bell,type=minecraft:interaction]'),
 'data get storage selftest:results']
fn('patterns',lines)
fn('death',['function selftest:spawn','kill @e[tag=nox.boss]'])
fn('result',[save('after_death_parts','execute if entity @e[tag=nox.bodypart]'),save('state_death','scoreboard players get #state nx.state'),'data get storage selftest:results'])
sector=[]
import math
for i in range(8):
 for label,offset,expected_safe in [('inside',0,True),('outside',45,False),('edge_inside',20,True),('edge_outside',25,False)]:
  a=math.radians(i*45+offset);x=math.cos(a)*12;z=math.sin(a)*12
  sector += [f'summon minecraft:marker {x:.4f} 81 {z:.4f} {{Tags:["test.sector"]}}',
   'scoreboard players set #x nx.tmp 0','scoreboard players set #z nx.tmp 0',
   f'execute as @e[tag=test.sector,limit=1] run function eclipse_nox:skills/sector/{i}',
   save(f'sector_{i}_{label}','execute if entity @e[tag=test.sector,tag=nox.shelter]'),
   'kill @e[tag=test.sector]']
fn('sectors',sector)
combat=[
 'tp @e[tag=nox.boss,limit=1] 0.0 81.0 0.0 0 0',
 'summon minecraft:marker 0.0 81.0 0.0 {Tags:["nox.owned","nox.target"],Rotation:[0f,0f]}',
 'execute at @e[tag=nox.anchor,tag=nox.current,limit=1] run function eclipse_nox:skills/dash/begin']
combat+=['execute as @e[tag=nox.anchor,tag=nox.current,limit=1] at @s run function eclipse_nox:skills/dash/tick']*18
combat += [save('dash_travel','data get entity @e[tag=nox.boss,limit=1] Pos[2] 10'),
 save('dash_finished','scoreboard players get #dash nx.dash'),save('dash_window','scoreboard players get #safe nx.safe'),
 'tp @e[tag=nox.boss,limit=1] 0.0 81.0 20.0 0 0',
 'summon minecraft:marker 0.0 81.0 20.0 {Tags:["nox.owned","nox.target"],Rotation:[0f,0f]}',
 'execute at @e[tag=nox.anchor,tag=nox.current,limit=1] run function eclipse_nox:skills/dash/begin',
 'execute as @e[tag=nox.anchor,tag=nox.current,limit=1] at @s run function eclipse_nox:skills/dash/tick',
 'execute as @e[tag=nox.anchor,tag=nox.current,limit=1] at @s run function eclipse_nox:skills/dash/tick',
 save('dash_wall_position','data get entity @e[tag=nox.boss,limit=1] Pos[2] 10'),
 save('dash_crash_window','scoreboard players get #safe nx.safe'),
 'scoreboard players set #counter nx.move 0','scoreboard players set #oldhp nx.hp 80000','scoreboard players set #safe nx.safe 60','scoreboard players set #expose nx.expose 1',
 'data modify entity @e[tag=nox.boss,limit=1] Health set value 760f',
 'execute as @e[tag=nox.anchor,tag=nox.current,limit=1] at @s run function eclipse_nox:fight/exposure',
 save('exposure_bonus_health','data get entity @e[tag=nox.boss,limit=1] Health'),
 'scoreboard players set #counter nx.move 1','scoreboard players set #oldhp nx.hp 80000','data modify entity @e[tag=nox.boss,limit=1] Health set value 760f',
 'function eclipse_nox:fight/exposure',save('counter_bonus_health','data get entity @e[tag=nox.boss,limit=1] Health'),
 'scoreboard players set #counter nx.move 0',
 'tp @e[tag=nox.boss,limit=1] 0.0 81.0 0.0 0 0',
 'summon minecraft:marker 0.0 81.0 0.0 {Tags:["nox.owned","nox.target"],Rotation:[0f,0f]}',
 'scoreboard players set #skill nx.skill 1','scoreboard players set #chain nx.combo 0','scoreboard players set #cast nx.cast 0',
 'execute as @e[tag=nox.anchor,tag=nox.current,limit=1] at @s run function eclipse_nox:skills/resolve',
 save('second_swing_warning','scoreboard players get #cast nx.cast'),
 'scoreboard players set #cast nx.cast 0',
 'execute as @e[tag=nox.anchor,tag=nox.current,limit=1] at @s run function eclipse_nox:skills/resolve',
 save('combo_recovery','scoreboard players get #safe nx.safe'),
 'data modify entity @e[tag=nox.boss,limit=1] Health set value 800f',
 'scoreboard players set #safe nx.safe 0','scoreboard players set #oldhp nx.hp -1','scoreboard players set #expose nx.expose 0']
combat += ['execute at @e[tag=nox.anchor,tag=nox.current,limit=1] run function eclipse_nox:minions/spawn', 'execute store result storage selftest:results minion_count int 1 run execute if entity @e[tag=nox.minion]',
 'execute store result storage selftest:results minion_models int 1 run execute if entity @e[tag=nox.minion_visual]',
 'execute at @e[tag=nox.anchor,tag=nox.current,limit=1] run function eclipse_nox:judgement/begin',
 save('judgement_warning','scoreboard players get #judgement nx.doom'),
 'execute at @e[tag=nox.anchor,tag=nox.current,limit=1] run function eclipse_nox:judgement/resolve',
 save('judgement_recovery','scoreboard players get #safe nx.safe'),
 'scoreboard players set #safe nx.safe 0','scoreboard players set #expose nx.expose 0',
 'scoreboard players set #adds nx.add 1198','execute at @e[tag=nox.anchor,tag=nox.current,limit=1] run function eclipse_nox:minions/tick',
 save('before_reinforcement_due','execute if entity @e[tag=nox.minion]'),
 'scoreboard players set #adds nx.add 1199','execute at @e[tag=nox.anchor,tag=nox.current,limit=1] run function eclipse_nox:minions/tick',
 save('periodic_living_reinforcement','execute if entity @e[tag=nox.minion]'),
 'function eclipse_nox:minions/spawn','function eclipse_nox:minions/spawn',
 save('uncapped_minions','execute if entity @e[tag=nox.minion]'),
 save('minion_passengers','execute if data entity @e[tag=nox.add.acolyte,limit=1] Passengers'),
 'damage @e[tag=nox.add.acolyte,limit=1] 4 minecraft:generic',
 save('minion_damage_health','data get entity @e[tag=nox.add.acolyte,limit=1] Health'),
 save('minion_scale','attribute @e[tag=nox.add.acolyte,limit=1] minecraft:scale get 100'),
 'function eclipse_nox:minions/boon_warden',save('warden_boon_pending','scoreboard players get #break nx.add'),
 'function eclipse_nox:minions/break',save('warden_boon_window','scoreboard players get #safe nx.safe'),
 save('warden_boon_counter','scoreboard players get #counter nx.move'),
 'scoreboard players set #safe nx.safe 0','scoreboard players set #counter nx.move 0','scoreboard players set #expose nx.expose 0',
 'scoreboard players set #team_acolyte nx.acolyte 0','scoreboard players set #team_adds nx.warden 0',
 'scoreboard players set @e[tag=nox.minion] nx.time 100000','execute at @e[tag=nox.anchor,tag=nox.current,limit=1] run function eclipse_nox:minions/tick',
 save('persistent_minions','execute if entity @e[tag=nox.minion]'),
 save('retire_no_kill_penalty','scoreboard players get #team_adds nx.warden'),
 'scoreboard players set #adds nx.add 1199','execute at @e[tag=nox.anchor,tag=nox.current,limit=1] run function eclipse_nox:minions/tick',
 save('next_periodic_wave','execute if entity @e[tag=nox.minion]'),
 'kill @e[tag=nox.minion]', 'function eclipse_nox:minions/tick',
 save('orphan_minion_models','execute if entity @e[tag=nox.minion_visual]')]
fn('combat',combat)
fn('progression',['summon minecraft:marker 0 81 0 {Tags:["test.progress"]}',
 'scoreboard players set @e[tag=test.progress] nx.wins 2',
 'execute as @e[tag=test.progress] run function eclipse_nox:challenge/reset_run',
 'scoreboard players set #window nx.window 1',
 'execute as @e[tag=test.progress] run function eclipse_nox:challenge/count_counter',
 'execute as @e[tag=test.progress] run function eclipse_nox:challenge/count_counter',
 save('counter_same_window','scoreboard players get @e[tag=test.progress,limit=1] nx.counter'),
 'scoreboard players set #window nx.window 2',
 'execute as @e[tag=test.progress] run function eclipse_nox:challenge/count_counter',
 save('counter_new_window','scoreboard players get @e[tag=test.progress,limit=1] nx.counter'),
 'execute as @e[tag=test.progress] run function eclipse_nox:challenge/reset_run',
 save('counter_run_reset','scoreboard players get @e[tag=test.progress,limit=1] nx.counter'),
 save('wins_persist','scoreboard players get @e[tag=test.progress,limit=1] nx.wins'),
 'kill @e[tag=test.progress]','scoreboard players set #mistakes nx.tmp 0'])
fn('cristiano',[
 'execute at @e[tag=db.anchor,limit=1] store result storage selftest:results cr_altar int 1 run execute if block ~ ~-1 ~ minecraft:gold_block',
 'execute at @e[tag=db.anchor,limit=1] store result storage selftest:results cr_center_trigger int 1 run execute if entity @e[tag=db.start,distance=..1]',
 'kill @e[tag=db.start]',
 'function desert_ball:tick',
 save('cr_trigger_repaired','execute if entity @e[tag=db.start]'),
 'execute at @e[tag=db.anchor,limit=1] run tag @e[tag=db.anchor,limit=1] add db.current',
 'execute at @e[tag=db.anchor,limit=1] run function desert_ball:fight/spawn',
 save('cr_boss','execute if entity @e[tag=db.boss]'),save('cr_parts','execute if entity @e[tag=db.body]'),
 save('cr_health','data get entity @e[tag=db.boss,limit=1] Health'),
 'scoreboard players set #hp db.hp 50000','scoreboard players set #max db.max 500',
 'scoreboard players set #cycle db.cycle 0','function desert_ball:skills/begin',
 save('cr_first_skill','scoreboard players get #skill db.skill'),
 'execute at @e[tag=db.boss,limit=1] run function desert_ball:skills/core_spawn',
 'damage @e[tag=db.core,limit=1] 2 minecraft:generic',
 'function desert_ball:skills/core_tick',save('cr_counter_window','scoreboard players get #safe db.safe'),
 save('cr_counter_cast','scoreboard players get #cast db.cast'),
 'execute at @e[tag=db.boss,limit=1] run function desert_ball:skills/shoot',
 'execute as @e[tag=db.shot] at @s run function desert_ball:shot/tick',
 save('cr_projectile','execute if entity @e[tag=db.shot]'),
 'execute at @e[tag=db.boss,limit=1] run function desert_ball:skills/overhead',
 save('cr_physical_body','data get entity @e[tag=db.boss,limit=1] attributes[{id:"minecraft:scale"}].base 100'),
 'function selftest:cr_motion',
 'summon minecraft:item_display ~ ~ ~ {Tags:["test.stack"],item:{id:"minecraft:diamond",count:5,components:{"minecraft:custom_data":{keep:73}}}}',
 'item modify entity @e[tag=test.stack,limit=1] contents desert_ball:take_one',
 save('cr_take_one_count','data get entity @e[tag=test.stack,limit=1] item.count'),
 save('cr_take_one_components','data get entity @e[tag=test.stack,limit=1] item.components."minecraft:custom_data".keep'),
 'kill @e[tag=test.stack]',
 'data merge storage desert_ball:capture {stack:{id:"minecraft:diamond",count:1,components:{"minecraft:custom_data":{keep:73},"minecraft:custom_name":{text:"분실물 테스트"}}},uuid:[I;1,2,3,4]}',
 'data modify storage desert_ball:ctx owner set value 123',
 'function desert_ball:theft/save with storage desert_ball:ctx',
 'data remove storage desert_ball:capture stack',
 'function desert_ball:theft/read with storage desert_ball:ctx',
 'execute at @e[tag=db.anchor,limit=1] run function desert_ball:theft/drop with storage desert_ball:capture',
 save('cr_refund_count','data get entity @e[tag=db.refund,limit=1] Item.count'),
 save('cr_refund_components','data get entity @e[tag=db.refund,limit=1] Item.components."minecraft:custom_data".keep'),
 'function desert_ball:theft/delete with storage desert_ball:ctx',
 save('cr_vault_cleared','execute unless data storage desert_ball:vault accounts.p123'),
 'function desert_ball:abort',
 save('cr_cleanup','execute unless entity @e[tag=db.boss]'),save('cr_cleanup_visual','execute unless entity @e[tag=db.visual]'),
 'kill @e[tag=db.refund]'])
from cristiano_art import MODES as CR_MODES, FRAMES as CR_FRAMES
cr_motion=[]
for mode in CR_MODES:
 for frame in range(CR_FRAMES):cr_motion.append(f'function desert_ball:visual/{mode}/{frame}')
cr_motion += ['scoreboard players set #time db.time 50','scoreboard players set #follow db.anim 0',
 'scoreboard players set #safe db.safe 0','scoreboard players set #cast db.cast 0',
 'scoreboard players set #skill db.skill 1','scoreboard players set #moving db.anim 0',
 'function desert_ball:visual/tick',save('cr_idle_mode','scoreboard players get #mode db.anim'),
 'scoreboard players set #moving db.anim 1','function desert_ball:visual/tick',
 save('cr_run_mode','scoreboard players get #mode db.anim'),
 'scoreboard players set #cast db.cast 12','function desert_ball:visual/tick',
 save('cr_shoot_mode','scoreboard players get #mode db.anim'),save('cr_shoot_frame','scoreboard players get #frame db.motion'),
 'scoreboard players set #skill db.skill 5','scoreboard players set #cast db.cast 11',
 'scoreboard players set #pending db.tmp 1','function desert_ball:skills/casting',
 save('cr_header_release','execute if entity @e[tag=db.shot,scores={db.skill=5}]'),
 save('cr_core_release','scoreboard players get #pending db.tmp'),
 'function desert_ball:visual/tick',save('cr_header_mode','scoreboard players get #mode db.anim'),
 'execute store result score #jump_y db.tmp run data get entity @e[tag=db.boss,limit=1] Pos[1] 100',
 'execute store result score #ground_y db.tmp run data get entity @e[tag=db.jump_origin,limit=1] Pos[1] 100',
 'scoreboard players operation #jump_y db.tmp -= #ground_y db.tmp',
 save('cr_header_jumped','execute if score #jump_y db.tmp matches 30..100'),
 'scoreboard players set #cast db.cast 1','function desert_ball:skills/casting',
 'execute store result score #jump_y db.tmp run data get entity @e[tag=db.boss,limit=1] Pos[1] 100',
 'scoreboard players operation #jump_y db.tmp -= #ground_y db.tmp',save('cr_header_landed','scoreboard players get #jump_y db.tmp'),
 'scoreboard players set #safe db.safe 0','scoreboard players set #skill db.skill 6',
 'scoreboard players set #cast db.cast 15','function desert_ball:skills/casting','function desert_ball:visual/tick',
 save('cr_overhead_mode','scoreboard players get #mode db.anim'),
 save('cr_overhead_release','execute if entity @e[tag=db.shot,scores={db.skill=6}]'),
 'function desert_ball:skills/counter',
 'execute store result score #jump_y db.tmp run data get entity @e[tag=db.boss,limit=1] Pos[1] 100',
 'scoreboard players operation #jump_y db.tmp -= #ground_y db.tmp',save('cr_counter_landed','scoreboard players get #jump_y db.tmp'),
 'function desert_ball:visual/tick',save('cr_stagger_mode','scoreboard players get #mode db.anim')]
fn('cr_motion',cr_motion)
from motion import MODES, FRAMES
animations=[]
for mode in MODES:
 for frame in range(FRAMES):animations.append(f'function eclipse_nox:visual/pose/{mode}/{frame}')
animations+=['function eclipse_nox:visual/pose/walk/4',
 save('left_leg_rotation','data get entity @e[tag=nox.joint.left_leg,limit=1] transformation.left_rotation[0] 1000'),
 save('right_leg_rotation','data get entity @e[tag=nox.joint.right_leg,limit=1] transformation.left_rotation[0] 1000')]
fn('animations',animations)
java=ROOT/'.tools/jdk25/jdk-25.0.4.1+1/bin/java.exe'
p=subprocess.Popen([str(java),'-javaagent:'+str(ROOT/'ida26/test-agent/test-network.jar'),'-Xms256M','-Xmx2G','-jar','server.jar','nogui'],cwd=SERVER,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
q=queue.Queue()
def pump():
 for line in p.stdout:q.put(line)
threading.Thread(target=pump,daemon=True).start()
commands=[('forceload add -32 -32 32 48',8),('execute positioned 0 81 0 run function eclipse_nox:admin/install',3),
 ('execute store result storage selftest:results entrance_open int 1 run execute if block 0 81 34 minecraft:air',.3),
 ('execute store result storage selftest:results arena_floor int 1 run execute if block 0 80 0 minecraft:deepslate_tiles',.3),
 ('execute store result storage selftest:results headroom int 1 run execute if block 0 97 0 minecraft:air',.3),
 ('function selftest:spawn',1),('function selftest:combat',1),('function selftest:progression',1),('function selftest:animations',1),('function selftest:phase2',1),('function selftest:patterns',1),('function selftest:sectors',1),('forceload add 96 -48 160 48',1),('execute positioned 128 81 0 run function desert_ball:admin/install',2),('function selftest:cristiano',1),('data get storage selftest:results',1),('function selftest:spawn',.3),('reload',4),
 ('execute store result storage selftest:results reload_cleanup int 1 run execute unless entity @e[tag=nox.boss]',.3),
 ('function selftest:death',3),('function selftest:result',1),('data get storage selftest:results',1),('stop',1)]
logpath=OUT/'engine-console.log';started=time.time();ready=False;index=0;nexttime=0
with logpath.open('w',encoding='utf-8') as log:
 while time.time()-started<240:
  try:line=q.get(timeout=.2)
  except queue.Empty:line=''
  if line:
   log.write(line);log.flush()
   if any(s in line for s in ['ERROR','Failed','Unknown','Done (','selftest:results','Stopping']):print(line.rstrip(),flush=True)
   if 'Done (' in line:ready=True;nexttime=time.time()+1
  if ready and index<len(commands) and time.time()>nexttime:
   cmd,delay=commands[index];p.stdin.write(cmd+'\n');p.stdin.flush();index+=1;nexttime=time.time()+delay
  if p.poll() is not None:break
 if p.poll() is None:
  p.stdin.write('stop\n');p.stdin.flush();p.wait(timeout=30)
clean=re.sub(r'\x1b\[[0-9;]*m','',logpath.read_text(encoding='utf-8'))
errors=[s for s in clean.splitlines() if 'Unable to locate English counter names in registry Perflib' not in s and any(k in s for k in ['ERROR','Failed to load function','Unknown or incomplete command','Incorrect argument','Unknown registry'])]
assert not errors,'\n'.join(errors[:30])
assert p.returncode==0 and 'Done (' in clean
expected={'boss_count':1,'health':800,'phase2':2,'shield':1,'step1':1,'step2':2,'step3':3,'unshield':0,'phase3':3,'overload':1,'expired_hazards':0,'after_abort':0,'after_abort_parts':0,'state_abort':0,'preserved_bells':3,'after_death_parts':0,'state_death':0}
expected.update({'minion_passengers':0,'minion_damage_health':24,'minion_scale':100,'warden_boon_pending':1,'warden_boon_window':40,'warden_boon_counter':1,'minion_count':2,'minion_models':0,'judgement_warning':40,'judgement_recovery':16,'uncapped_minions':8,'before_reinforcement_due':2,'periodic_living_reinforcement':4,'persistent_minions':8,'retire_no_kill_penalty':0,'next_periodic_wave':10,'orphan_minion_models':0})
expected.update({'counter_same_window':1,'counter_new_window':2,'counter_run_reset':0,'wins_persist':2})
expected.update({'cr_boss':1,'cr_parts':13,'cr_health':500,'cr_first_skill':1,'cr_counter_window':40,'cr_counter_cast':0,'cr_projectile':1,'cr_physical_body':130,'cr_take_one_count':4,'cr_take_one_components':73,'cr_refund_count':1,'cr_refund_components':73,'cr_vault_cleared':1,'cr_cleanup':1,'cr_cleanup_visual':1})
expected.update({'cr_altar':1,'cr_center_trigger':0,'cr_trigger_repaired':0})
expected.update({'cr_idle_mode':0,'cr_run_mode':1,'cr_shoot_mode':2,'cr_shoot_frame':11,'cr_header_mode':6,'cr_header_release':1,'cr_core_release':0,'cr_header_jumped':1,'cr_header_landed':0,'cr_overhead_mode':7,'cr_overhead_release':1,'cr_counter_landed':0,'cr_stagger_mode':8})
expected.update({'visuals':10,'entrance_open':1,'arena_floor':1,'headroom':1})
expected.update({'dash_travel':144,'dash_finished':0,'dash_window':16,'dash_wall_position':208,'dash_crash_window':40,'exposure_bonus_health':740,'counter_bonus_health':720,'second_swing_warning':10,'combo_recovery':12,'reload_cleanup':1})
for i in range(8):
 for label,value in [('inside',1),('outside',0),('edge_inside',1),('edge_outside',0)]:expected[f'sector_{i}_{label}']=value
for k,v in expected.items():assert re.search(r'\b'+k+r': '+str(v)+r'\b',clean),(k,v)
left=int(re.search(r'left_leg_rotation: (-?\d+)',clean)[1]);right=int(re.search(r'right_leg_rotation: (-?\d+)',clean)[1]);assert left>200 and right<-200,(left,right)
js(OUT/'engine-validation.json',{'revision':2,'engine':'Official vanilla Minecraft Java 26.3','world':WORLD,'command_errors':0,'assertions':expected,'animation_pose_functions_executed':len(MODES)*FRAMES,'opposed_leg_rotation_verified':True,'datapack_sha256':sha(OUT/'Nox-Standalone-Datapack-26.3.zip'),'network_disabled_for_local_test_only':True,'limitations':['No connected players: right-click routing, combat damage, reconnect exclusion, client rendering and party balance require playtesting.']})
print('Nox engine validation passed.',flush=True)
