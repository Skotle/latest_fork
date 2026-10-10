"""Test all six skills using an in-process vanilla ServerPlayer, no network client."""
import json,queue,re,shutil,subprocess,threading,time,zipfile
from pathlib import Path
from build import BASE,ROOT,OUT,js,sha
SERVER=BASE/'frost-player-test';SERVER.mkdir(exist_ok=True)
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
 'online-mode=false','server-ip=127.0.0.1','server-port=25594','view-distance=3','simulation-distance=3','spawn-protection=0','difficulty=normal','max-tick-time=-1'])+'\n')
test=dest/'selftest';js(test/'pack.mcmeta',{'pack':{'min_format':[121,0],'max_format':[121,0],'description':'Actual vanilla ServerPlayer probe'}})
fns=test/'data/selftest/function';fns.mkdir(parents=True)
def fn(name,lines):(fns/(name+'.mcfunction')).write_text('\n'.join(lines)+'\n',encoding='utf-8')
def save(key,cmd):return 'execute store result storage selftest:results '+key+' int 1 run '+cmd

fn('setup',['time set noon','weather clear','forceload add 96 -32 160 48','execute positioned 128 81 0 run function frost_warden:admin/install','tp @a[tag=probe.player] 128 81 -12','execute positioned 128 81 0 run function frost_warden:admin/summon','function frost_warden:tick',
 save('boss','execute if entity @e[tag=fw.boss]'),save('health','scoreboard players get #max fw.max'),save('bow','execute if items entity @e[tag=fw.boss,limit=1] weapon.mainhand minecraft:bow'),
 'scoreboard players set #next fw.next 99999','scoreboard players set #safe fw.safe 99999','scoreboard players set #blink fw.blink 99999','data merge entity @e[tag=fw.boss,limit=1] {NoAI:1b}',
 'damage @e[tag=fw.boss,limit=1] 10 minecraft:fall'])
fn('armor_equip',['attribute @a[tag=probe.player,limit=1] minecraft:knockback_resistance base set 1','summon minecraft:pig 130 81 -6 {Tags:["probe.attacker"],NoAI:1b,NoGravity:1b,PersistenceRequired:1b}','tag @a[tag=probe.player] add probe.armor_sample','tag @a[tag=probe.player] add probe.shield','tag @a[tag=probe.player] add probe.heal','item replace entity @a[tag=probe.player,limit=1] armor.head with minecraft:leather_helmet'])
fn('armor_base',[save('armor_base_before','data get entity @a[tag=probe.player,limit=1] Health 1000'),'damage @a[tag=probe.player,limit=1] 100 minecraft:arrow by @e[tag=fw.boss,limit=1]'])
fn('armor_normal',[save('control_actor','execute if entity @e[tag=probe.attacker]'),save('armor_base_after','data get entity @a[tag=probe.player,limit=1] Health 1000'),'item replace entity @a[tag=probe.player,limit=1] armor.head with minecraft:leather_helmet[minecraft:enchantments={"minecraft:projectile_protection":4}]',save('pp_normal_before','data get entity @a[tag=probe.player,limit=1] Health 1000'),save('control_damage_success','damage @a[tag=probe.player,limit=1] 100 minecraft:arrow by @e[tag=probe.attacker,limit=1]')])
fn('armor_boss',[save('pp_normal_after','data get entity @a[tag=probe.player,limit=1] Health 1000'),save('pp_boss_before','data get entity @a[tag=probe.player,limit=1] Health 1000'),'damage @a[tag=probe.player,limit=1] 100 minecraft:arrow by @e[tag=fw.boss,limit=1]'])
fn('general_normal',[save('pp_boss_after','data get entity @a[tag=probe.player,limit=1] Health 1000'),'item replace entity @a[tag=probe.player,limit=1] armor.head with minecraft:leather_helmet[minecraft:enchantments={"minecraft:protection":4}]',save('general_normal_before','data get entity @a[tag=probe.player,limit=1] Health 1000'),save('control_damage_success','damage @a[tag=probe.player,limit=1] 100 minecraft:arrow by @e[tag=probe.attacker,limit=1]')])
fn('general_boss',[save('general_normal_after','data get entity @a[tag=probe.player,limit=1] Health 1000'),save('general_boss_before','data get entity @a[tag=probe.player,limit=1] Health 1000'),'damage @a[tag=probe.player,limit=1] 100 minecraft:arrow by @e[tag=fw.boss,limit=1]'])
fn('full_equip',[save('general_boss_after','data get entity @a[tag=probe.player,limit=1] Health 1000'),*[f'item replace entity @a[tag=probe.player,limit=1] armor.{slot} with minecraft:leather_{item}' for slot,item in [('head','helmet'),('chest','chestplate'),('legs','leggings'),('feet','boots')]]])
fn('full_base',[save('full_base_before','data get entity @a[tag=probe.player,limit=1] Health 1000'),'damage @a[tag=probe.player,limit=1] 100 minecraft:arrow by @e[tag=fw.boss,limit=1]'])
fn('full_normal',[save('full_base_after','data get entity @a[tag=probe.player,limit=1] Health 1000'),*[f'item replace entity @a[tag=probe.player,limit=1] armor.{slot} with minecraft:leather_{item}[minecraft:enchantments={{"minecraft:projectile_protection":4}}]' for slot,item in [('head','helmet'),('chest','chestplate'),('legs','leggings'),('feet','boots')]],save('full_normal_before','data get entity @a[tag=probe.player,limit=1] Health 1000'),save('control_damage_success','damage @a[tag=probe.player,limit=1] 100 minecraft:arrow by @e[tag=probe.attacker,limit=1]')])
fn('full_boss',[save('full_normal_after','data get entity @a[tag=probe.player,limit=1] Health 1000'),save('full_boss_before','data get entity @a[tag=probe.player,limit=1] Health 1000'),'damage @a[tag=probe.player,limit=1] 100 minecraft:arrow by @e[tag=fw.boss,limit=1]'])
fn('armor_restore',[save('full_boss_after','data get entity @a[tag=probe.player,limit=1] Health 1000'),*[f'item replace entity @a[tag=probe.player,limit=1] armor.{slot} with minecraft:air' for slot in ['head','chest','legs','feet']],'tag @a[tag=probe.player] add probe.heal','tp @a[tag=probe.player] 128 81 -12','tag @a[tag=probe.player] remove probe.shield','kill @e[tag=probe.attacker]'])
fn('patterns',[save('pool_after_hit','scoreboard players get #pool fw.hp'),save('body_restored','data get entity @e[tag=fw.boss,limit=1] Health'),
 'tp @e[tag=fw.boss,limit=1] 128 81 -2','execute at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ rotated 180 0 run function frost_warden:skills/fan',save('fan','execute if entity @e[tag=fw.arrow]'),'kill @e[tag=fw.arrow]',
 'scoreboard players set #focus fw.tmp 4','scoreboard players set #cycle fw.cycle 4','function frost_warden:skills/begin',save('focus_skill','scoreboard players get #skill fw.skill'),save('focus_spent','scoreboard players get #focus fw.tmp'),
 *['function frost_warden:skills/casting']*24,save('focus_arrows','execute if entity @e[tag=fw.arrow,nbt={PierceLevel:0b}]'),save('focus_damage','data get entity @e[tag=fw.arrow,limit=1] damage 1000'),'kill @e[tag=fw.arrow]',
 'function frost_warden:ashe/walls_select',save('wall_side_a','execute if entity @e[tag=fw.wall_live]'),'function frost_warden:walls/wave_one',save('wall_arrows','execute if entity @e[tag=fw.wall_arrow]'),'kill @e[tag=fw.arrow]','function frost_warden:ashe/walls_select',save('wall_side_b','execute if entity @e[tag=fw.wall_live]'),
 'scoreboard players set #cast fw.cast 0','scoreboard players set #safe fw.safe 99999','scoreboard players set #next fw.next 99999',
 'scoreboard players operation #probe_pool fw.hp = #pool fw.hp','execute positioned 128 82 -8 rotated 0 0 run function frost_warden:arrows/normal'])
fn('own_result',[save('own_immune','execute if score #pool fw.hp = #probe_pool fw.hp'),'kill @e[tag=fw.arrow]',
 'data modify storage selftest:shot owner set from entity @a[tag=probe.player,limit=1] UUID','function selftest:external_arrow with storage selftest:shot'])
fn('external_arrow',['$summon minecraft:arrow 128 82 -8 {Tags:["probe.external"],Owner:$(owner),Motion:[0d,0d,2d],damage:1.6d,PierceLevel:0b,pickup:0b,item:{id:"minecraft:arrow",count:1}}'])
fn('external_result',[save('external_hits','execute if score #pool fw.hp < #probe_pool fw.hp'),save('hawk_before','data get entity @a[tag=probe.player,limit=1] Health 10'),
 'scoreboard players set #cycle fw.cycle 5','function frost_warden:skills/begin',save('hawk','execute if entity @e[tag=fw.hawk]'),'scoreboard players set #cast fw.cast 0','scoreboard players set #safe fw.safe 99999','scoreboard players set #next fw.next 99999'])
fn('hawk_check',[save('hawk_after','data get entity @a[tag=probe.player,limit=1] Health 10'),save('revealed','execute if entity @a[tag=fw.revealed]'),save('hawk_finished','execute unless entity @e[tag=fw.hawk]'),
 'attribute @a[tag=probe.player,limit=1] minecraft:knockback_resistance base set 1','item replace entity @a[tag=probe.player,limit=1] weapon.offhand with minecraft:shield','tp @a[tag=probe.player] 128 81 -12 0 0','tag @a[tag=probe.player] add probe.shield'])
fn('normal_shot',[save('normal_before','data get entity @a[tag=probe.player,limit=1] Health 10'),'execute positioned 128 82 -8 rotated 180 0 run function frost_warden:arrows/normal'])
fn('ultimate',[save('normal_after','data get entity @a[tag=probe.player,limit=1] Health 10'),'kill @e[tag=fw.arrow]',
 'scoreboard players set #cycle fw.cycle 8','function frost_warden:skills/begin',*['function frost_warden:skills/casting']*15,save('ultimate_charge_clear','execute unless entity @e[tag=fw.stun_arrow]'),
 'function frost_warden:skills/casting',save('ultimate_one','execute if entity @e[tag=fw.stun_arrow,nbt={PierceLevel:1b,damage:6.5d}]'),save('ultimate_before','data get entity @a[tag=probe.player,limit=1] Health 10'),
 'scoreboard players set #cast fw.cast 0','scoreboard players set #safe fw.safe 99999','scoreboard players set #next fw.next 99999'])
fn('stun_check',[save('ultimate_after','data get entity @a[tag=probe.player,limit=1] Health 10'),save('stunned','execute if entity @a[tag=fw.stunned]'),save('stun_speed','attribute @a[tag=probe.player,limit=1] minecraft:movement_speed get 1000'),save('no_blindness','execute unless entity @a[nbt={active_effects:[{id:"minecraft:blindness"}]}]'),
 'tag @a[tag=probe.player] remove probe.shield','item replace entity @a[tag=probe.player,limit=1] weapon.offhand with minecraft:air'])
fn('mobility',[save('mobility_restored','execute unless entity @a[tag=fw.stunned] unless entity @a[tag=fw.bound] unless entity @a[nbt={active_effects:[{id:"minecraft:slowness",amplifier:6b}]}]'),
 'execute as @a[tag=probe.player] run function frost_warden:stun/hit',save('stun_guard','execute unless entity @a[tag=fw.stunned]'),
 'tp @a[tag=probe.player] 128 81 -8','execute as @a[tag=probe.player] at @s run function frost_warden:stun/apply',save('stun_near','scoreboard players get @a[tag=probe.player,limit=1] fw.stun'),'execute as @a[tag=probe.player] run function frost_warden:stun/end',
 'tp @a[tag=probe.player] 128 81 -12','execute as @a[tag=probe.player] at @s run function frost_warden:stun/apply',save('stun_medium','scoreboard players get @a[tag=probe.player,limit=1] fw.stun'),'execute as @a[tag=probe.player] run function frost_warden:stun/end',
 'tp @a[tag=probe.player] 128 81 -24','execute as @a[tag=probe.player] at @s run function frost_warden:stun/apply',save('stun_far','scoreboard players get @a[tag=probe.player,limit=1] fw.stun'),'execute as @a[tag=probe.player] run function frost_warden:stun/end','tp @a[tag=probe.player] 128 81 -12',
 'scoreboard players set #skill fw.skill 4','function frost_warden:skills/recover',save('ultimate_recovery','scoreboard players get #safe fw.safe'),
 'scoreboard players set #time fw.time 1800','scoreboard players set #pool fw.hp 25000','scoreboard players set #safe fw.safe 0','scoreboard players set #next fw.next 0','scoreboard players set #cycle fw.cycle 0','scoreboard players set #focus fw.tmp 0',
 'scoreboard players set #blink fw.blink 1','scoreboard players set #teleports fw.tmp 0','scoreboard objectives add probe.seen dummy',*[f'scoreboard players set #{i} probe.seen 0' for i in range(1,7)],'scoreboard players set #legacy_hazards probe.seen 0'])
fn('tick',[*[f'execute if score #state fw.state matches 1 if score #skill fw.skill matches {i} if score #cast fw.cast matches 1.. run scoreboard players set #{i} probe.seen 1' for i in range(1,7)],
 'execute if entity @e[tag=fw.bomb_mark] run scoreboard players set #legacy_hazards probe.seen 1','execute if entity @e[tag=fw.ring] run scoreboard players set #legacy_hazards probe.seen 1','execute if entity @e[tag=fw.explosive] run scoreboard players set #legacy_hazards probe.seen 1'])
js(test/'data/minecraft/tags/function/tick.json',{'values':['selftest:tick']})
fn('results',[save('walked','execute if score #steps fw.walk matches 20..'),*[save('seen_'+str(i),f'scoreboard players get #{i} probe.seen') for i in range(1,7)],save('legacy_hazards','scoreboard players get #legacy_hazards probe.seen'),save('no_permanent_slow','execute unless entity @a[tag=fw.bound] unless entity @a[nbt={active_effects:[{id:"minecraft:slowness",duration:-1}]}]'),
 save('phase','scoreboard players get #phase fw.phase'),save('adds','execute if entity @e[tag=fw.add]'),save('teleported','execute if score #teleports fw.tmp matches 1..'),save('sun_helmet','execute if items entity @e[tag=fw.boss,limit=1] armor.head minecraft:iron_helmet[minecraft:unbreakable]'),
 'scoreboard players add @a[tag=probe.player] nx.death 1','function frost_warden:fight/tick',save('death_cleanup','execute unless entity @a[tag=fw.stunned] unless entity @a[tag=fw.bound]'),'scoreboard players operation @a[tag=probe.player] fw.olddeath = @a[tag=probe.player] nx.death','function frost_warden:fight/tick',
 'function frost_warden:abort',save('cleanup','execute unless entity @e[tag=fw.owned]'),
 'summon minecraft:arrow 128 82.5 5 {Tags:["probe.startarrow"],Motion:[0d,0d,-2d],pickup:0b,item:{id:"minecraft:arrow",count:1}}'])
fn('activation',[save('target_start','execute if entity @e[tag=fw.boss]'),'scoreboard players set #pool fw.hp 0'])
fn('reward',[save('won','execute if entity @a[tag=probe.player,advancements={frost_warden:victory=true}]'),save('emeralds','clear @a[tag=probe.player] minecraft:emerald 0'),save('won_cleanup','execute unless entity @e[tag=fw.owned]'),'data get storage selftest:results'])
p=subprocess.Popen([str(java),'-javaagent:'+str(agent),'-Xms256M','-Xmx2G','-cp',classpath+';'+str(agent),'net.minecraft.server.Main','nogui'],
 cwd=SERVER,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
q=queue.Queue()
def pump():
 for line in p.stdout:q.put(line)
threading.Thread(target=pump,daemon=True).start()
commands=[('function selftest:setup',2),('function selftest:armor_equip',1.2),('function selftest:armor_base',1.2),('function selftest:armor_normal',1.2),('function selftest:armor_boss',1.2),('function selftest:general_normal',1.2),('function selftest:general_boss',1.2),('function selftest:full_equip',1.2),('function selftest:full_base',1.2),('function selftest:full_normal',1.2),('function selftest:full_boss',1.2),('function selftest:armor_restore',1),('function selftest:patterns',1),('function selftest:own_result',1),('function selftest:external_result',2),('function selftest:hawk_check',1),('function selftest:normal_shot',1),('function selftest:ultimate',.4),('function selftest:stun_check',2),('function selftest:mobility',45),('function selftest:results',2),('function selftest:activation',1),('function selftest:reward',1),('data get storage selftest:results',1),('stop',0)]
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
clean=''.join(log);(OUT/'Frost-player-console.log').write_text(clean,encoding='utf-8')
assert p.returncode==0 and ready,clean[-6000:]

expected={'walked':1,'control_actor':1,'control_damage_success':1,'boss':1,'health':900,'bow':1,'pool_after_hit':89000,'body_restored':1000,'fan':9,'focus_skill':2,'focus_spent':0,'focus_arrows':5,'focus_damage':2400,'wall_side_a':16,'wall_side_b':16,'wall_arrows':16,'own_immune':1,'external_hits':1,'hawk':1,'revealed':1,'hawk_finished':1,'ultimate_charge_clear':1,'ultimate_one':1,'stunned':1,'stun_speed':0,'no_blindness':1,'mobility_restored':1,'stun_guard':1,'stun_near':10,'stun_medium':20,'stun_far':30,'ultimate_recovery':24,'legacy_hazards':0,'no_permanent_slow':1,'phase':3,'adds':1,'teleported':1,'sun_helmet':1,'death_cleanup':1,'cleanup':1,'target_start':1,'won':1,'emeralds':12,'won_cleanup':1,**{'seen_'+str(i):1 for i in range(1,7)}}
for k,v in expected.items():assert re.search(r'\b'+k+r': '+str(v)+r'\b',clean),(k,v,clean[-7000:])
def val(k):return int(re.search(r'\b'+k+r': (\d+)',clean)[1])
assert val('normal_before')==val('normal_after')
assert val('ultimate_before')-val('ultimate_after')==130
assert val('hawk_before')==val('hawk_after')
def damage(key):return (val(key+'_before')-val(key+'_after'))/1000
base=damage('armor_base'); full=damage('full_base')
assert abs(damage('pp_normal')/base-.68)<.002
assert abs(damage('pp_boss')/base-.84)<.002
assert abs(damage('general_normal')-damage('general_boss'))<.002
assert abs(damage('general_boss')/base-.84)<.002
assert abs(damage('full_normal')/full-.2)<.002
assert abs(damage('full_boss')/full-.36)<.002
protection_probe={'single_IV_normal_reduction':1-damage('pp_normal')/base,'single_IV_boss_reduction':1-damage('pp_boss')/base,'full_IV_normal_reduction':1-damage('full_normal')/full,'full_IV_boss_reduction':1-damage('full_boss')/full,'general_protection_normal_damage':damage('general_normal'),'general_protection_boss_damage':damage('general_boss'),'epf_contribution_halved':True}
errors=[l for l in clean.splitlines() if 'ERROR' in l and 'Perflib' not in l]
assert not errors,errors
js(OUT/'Frost-player-validation.json',{'engine':'Vanilla Java 26.3 in-process ServerPlayer','revision':23,'projectile_protection_comparison':protection_probe,'assertions':expected,'six_skills_seen_in_live_tick_loop':True,'normal_arrow_blocked_by_shield':True,'ultimate_shield_damage':13,'stun_finite_and_distance_scaled':True,'permanent_slowness_removed':True,'old_overlapping_hazards_disabled':True,'own_physical_arrows_rejected':True,'player_physical_arrows_damage_boss':True,'datapack_sha256':sha(OUT/'Nox-Standalone-Datapack-26.3.zip'),'limitations':['Packets suppressed; connected-client rendering and difficulty balance still need playtesting.']})
print('Ashe-inspired frost combat/finite-stun probe passed.')
