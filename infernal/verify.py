"""Boot a fresh official 26.3 server; verify pack parsing and real entity state."""
import hashlib,json,queue,re,shutil,subprocess,threading,time
from pathlib import Path
BASE=Path(__file__).resolve().parent;ROOT=BASE.parent
work=BASE/'test-server';work.mkdir(exist_ok=True)
world='verify-'+str(int(time.time()));dest=work/world/'datapacks';dest.mkdir(parents=True)
shutil.copy2(BASE/'output/Infernal-Difficulties-26.3.zip',dest/'Infernal.zip')
(work/'eula.txt').write_text('eula=true\n')
(work/'server.properties').write_text('\n'.join(['level-name='+world,'level-type=minecraft:flat','generate-structures=false','online-mode=false','server-ip=127.0.0.1','server-port=25619','view-distance=2','simulation-distance=2','spawn-protection=0','difficulty=hard','max-tick-time=-1'])+'\n')
java=ROOT/'.tools/jdk25/jdk-25.0.4.1+1/bin/java.exe'
with (work/'server.properties').open('a') as config:
 config.write('generator-settings={"layers":[{"block":"minecraft:bedrock","height":1},{"block":"minecraft:stone","height":2}],"biome":"minecraft:plains"}\n')
p=subprocess.Popen([str(java),'-Djava.net.preferIPv4Stack=true','-Djdk.net.unixdomain.tmpdir=','-Djava.nio.channels.spi.SelectorProvider=sun.nio.ch.WindowsSelectorProvider','-XX:ActiveProcessorCount=4','-Xms256M','-Xmx1G','-jar',str(ROOT/'nox/frost-worldgen-test/server.jar'),'nogui'],cwd=work,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
q=queue.Queue()
def pump():
 for line in p.stdout:q.put(line)
threading.Thread(target=pump,daemon=True).start()
commands=[('forceload add 0 0',1),('summon zombie 0 100 0 {Tags:["test.zombie"],NoAI:1b,PersistenceRequired:1b}',1),('function infernal:set/nightmare',1),('attribute @e[tag=test.zombie,limit=1] minecraft:max_health get',0),('data get entity @e[tag=test.zombie,limit=1] Health',0),('attribute @e[tag=test.zombie,limit=1] minecraft:attack_damage get',0),('function infernal:set/demon',1),('attribute @e[tag=test.zombie,limit=1] minecraft:max_health get',0),('function infernal:set/hard',1),('attribute @e[tag=test.zombie,limit=1] minecraft:max_health get',0),('data get entity @e[tag=test.zombie,limit=1] Health',0),('summon creeper 2 100 0 {Tags:["test.creeper"],NoAI:1b}',0),('function infernal:set/nightmare',1),('data get entity @e[tag=test.creeper,limit=1] Fuse',0),('function infernal:set/easy',1),('data get entity @e[tag=test.creeper,limit=1] Fuse',0),('function infernal:menu',0),('stop',0)]
commands.insert(0,('time set midnight',0))
extra=[]
def check(cmd,expected,label):
 extra.extend([(f'execute store result score #test inf.sys run {cmd}',0),(f'execute unless score #test inf.sys matches {expected} run say TEST_FAIL_{label}',0),(f'execute if score #test inf.sys matches {expected} run say TEST_PASS_{label}',0)])
extra += [('function infernal:set/hard',.5),('summon zombie 5 100 0 {Tags:["test.gear"],NoAI:1b,PersistenceRequired:1b,equipment:{head:{id:"minecraft:diamond_helmet",count:1}},drop_chances:{head:0.75f}}',.5),('function infernal:set/nightmare',.5),('execute as @e[tag=test.gear,limit=1] run function infernal:piece/nightmare_feet_iron',0),('function infernal:set/hard',.5)]
check('execute if data entity @e[tag=test.gear,limit=1] equipment.head{id:"minecraft:diamond_helmet"}',1,'original_helmet')
check('execute if data entity @e[tag=test.gear,limit=1] equipment.feet.id',0,'added_boots_removed')
for mode,hp in [('harder',2400),('insane',2800),('demon',3200),('nightmare',4000)]:
 extra += [('function infernal:set/'+mode,.5)]
 check('attribute @e[tag=test.zombie,limit=1] minecraft:max_health get 100',hp,'hp_'+mode)
extra += [('reload',1)]
check('attribute @e[tag=test.zombie,limit=1] minecraft:max_health get 100',4000,'reload_no_stack')
extra += [('summon elder_guardian 8 100 0 {Tags:["test.boss"],NoAI:1b}',1)]
check('attribute @e[tag=test.boss,limit=1] minecraft:max_health get 100',12000,'boss')
extra += [('summon zombie 10 100 0 {Tags:["infernal.exclude","test.exclude"],NoAI:1b}',1)]
check('attribute @e[tag=test.exclude,limit=1] minecraft:max_health get 100',2000,'excluded')
extra += [('summon zombie 12 100 0 {Tags:["test.cap"],NoAI:1b,attributes:[{id:"minecraft:follow_range",base:60}]}',1)]
check('attribute @e[tag=test.cap,limit=1] minecraft:follow_range get 100',6400,'follow_cap')
extra += [('function infernal:set/hard',.5)]
check('attribute @e[tag=test.cap,limit=1] minecraft:follow_range get 100',6000,'follow_restore')
for mode,value in [('peaceful',0),('easy',1),('normal',2),('hard',3)]:
 extra += [('function infernal:set/'+mode,.5)]
 check('difficulty',value,'difficulty_'+mode)
commands[-1:-1]=extra
log=[];start=time.time();index=0;ready=False;nexttime=0
while time.time()-start<180:
 try:
  line=q.get(timeout=.1);log.append(line)
  if 'ERROR' in line or 'Failed' in line:print(line.strip(),flush=True)
  if 'Done (' in line:ready=True;nexttime=time.time()+1
 except queue.Empty:pass
 if ready and index<len(commands) and time.time()>=nexttime:
  cmd,delay=commands[index];p.stdin.write(cmd+'\n');p.stdin.flush();index+=1;nexttime=time.time()+max(.2,delay)
 if p.poll() is not None:break
else:p.kill();raise RuntimeError('server timeout')
text=''.join(log);(BASE/'output/validation-console.log').write_text(text,encoding='utf-8')
assert ready and p.returncode==0,text[-4000:]
assert not re.search(r'Failed to (load|parse)|Parsing error|Unknown function',text),text[-6000:]
assert '40.0' in text and '32.0' in text and '20.0' in text,text[-6000:]
assert '20s' in text and '30s' in text,text[-6000:]
assert 'TEST_FAIL_' not in text,text[-9000:]
assert text.count('TEST_PASS_')==15,text[-9000:]
(BASE/'output/validation.json').write_text(json.dumps({'server':'26.3','pack_loaded':True,'assertions_passed':15,'datapack_sha256':hashlib.sha256((BASE/'output/Infernal-Difficulties-26.3.zip').read_bytes()).hexdigest(),'nightmare_hp':40,'demon_hp':32,'restored_hp':20,'nightmare_fuse':20,'restored_fuse':30,'checks':['four_custom_hp_presets','four_vanilla_difficulty_presets','equipment_restore','reload_no_stacking','boss_hp','exclude_tag','follow_cap_and_restore']},indent=2))
print(text[-6000:])
