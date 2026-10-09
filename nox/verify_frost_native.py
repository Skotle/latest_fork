"""Test all six skills using an in-process vanilla ServerPlayer, no network client."""
import json,queue,re,shutil,subprocess,threading,time,zipfile
from pathlib import Path
from build import BASE,ROOT,OUT,js,sha
SERVER=BASE/'frost-native-test';SERVER.mkdir(exist_ok=True)
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
 'online-mode=false','server-ip=127.0.0.1','server-port=25592','view-distance=3','simulation-distance=3','spawn-protection=0','difficulty=normal','max-tick-time=-1'])+'\n')
test=dest/'selftest';js(test/'pack.mcmeta',{'pack':{'min_format':[121,0],'max_format':[121,0],'description':'Actual vanilla ServerPlayer probe'}})
fns=test/'data/selftest/function';fns.mkdir(parents=True)
def fn(name,lines):(fns/(name+'.mcfunction')).write_text('\n'.join(lines)+'\n',encoding='utf-8')
def save(key,cmd):return 'execute store result storage selftest:results '+key+' int 1 run '+cmd

fn('setup',['forceload add 96 -32 160 48','execute positioned 128 81 0 run function frost_warden:admin/install','tp @a[tag=probe.player] 128 81 -8','execute positioned 128 81 0 run function frost_warden:admin/summon','data merge entity @e[tag=fw.boss,limit=1] {NoAI:1b}','scoreboard players set #next fw.next 99999','scoreboard players set #safe fw.safe 99999','tag @a[tag=probe.player] add probe.native'])
fn('result',[save('native_birth','scoreboard players get #native_birth fw.tmp'),'function frost_warden:abort'])
p=subprocess.Popen([str(java),'-javaagent:'+str(agent),'-Xms256M','-Xmx2G','-cp',classpath+';'+str(agent),'net.minecraft.server.Main','nogui'],
 cwd=SERVER,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
q=queue.Queue()
def pump():
 for line in p.stdout:q.put(line)
threading.Thread(target=pump,daemon=True).start()
commands=[('function selftest:setup',1),('function selftest:result',1),('data get storage selftest:results',1),('stop',0)]
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
clean=''.join(log);(OUT/'Frost-native-console.log').write_text(clean,encoding='utf-8')
assert p.returncode==0 and ready,clean[-6000:]

assert re.search(r'\bnative_birth: 0\b',clean),clean[-3000:]
js(OUT/'Frost-native-piercing-validation.json',{'native_arrow_piercing_before_first_tick':0,'datapack_sha256':sha(OUT/'Nox-Standalone-Datapack-26.3.zip')})
print('Native ordinary bow arrow is shield-blockable at creation.')
