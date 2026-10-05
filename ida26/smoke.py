import json, pathlib, queue, shutil, subprocess, threading, time
BASE=pathlib.Path(__file__).resolve().parent; ROOT=BASE.parent
SERVER=ROOT/'.tools/ida263-smoke'
world='test-'+str(int(time.time()))
(SERVER/world/'datapacks').mkdir(parents=True)
props=(SERVER/'server.properties').read_text()
import re
(SERVER/'server.properties').write_text(re.sub(r'(?m)^level-name=.*$', 'level-name='+world,props))
shutil.copy2(BASE/'output/IDA-Vanilla-26.3.zip',SERVER/world/'datapacks/IDA-Vanilla-26.3.zip')
test=SERVER/world/'datapacks/selftest';(test/'data/selftest/function').mkdir(parents=True)
(test/'pack.mcmeta').write_text(json.dumps({'pack':{'min_format':[121,0],'max_format':[121,0],'description':'Temporary IDA validation'}}))
loot_commands=[]
for f in sorted((BASE/'pack/data/dungeons_arise/loot_table').rglob('*.json')):
 ident=f.relative_to(BASE/'pack/data/dungeons_arise/loot_table').with_suffix('').as_posix()
 loot_commands.append('loot spawn 0 80 0 loot dungeons_arise:'+ident)
(test/'data/selftest/function/loot_all.mcfunction').write_text('\n'.join(loot_commands)+'\n')
java=ROOT/'.tools/jdk25/jdk-25.0.4.1+1/bin/java.exe'
p=subprocess.Popen([str(java),'-javaagent:'+str(BASE/'test-agent/test-network.jar'),'-Djava.net.preferIPv4Stack=true','-Dio.netty.transport.noNative=true','-Xms256M','-Xmx3G','-jar','paper.jar','--nogui'],cwd=SERVER,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',bufsize=1)
q=queue.Queue()
def pump():
 for line in p.stdout:q.put(line)
threading.Thread(target=pump,daemon=True).start()
def command(cmd):p.stdin.write(cmd+'\n');p.stdin.flush()
log=BASE/'output/smoke-console.log';start=time.time();started=False;steps=0;next_step=0
commands=['datapack list enabled','reload','forceload add -256 -256 -1 -1','forceload add 0 -256 255 -1','forceload add -256 0 -1 255','forceload add 0 0 255 255']
for i,f in enumerate(sorted((BASE/'pack/data/dungeons_arise/worldgen/structure').glob('*.json'))):
 commands.append(f'execute positioned 0 80 0 run place structure dungeons_arise:{f.stem}')
commands+=['execute positioned 0 80 0 run function selftest:loot_all', 'execute positioned 0 80 0 run function dungeons_arise:discharge_ready','stop']
with log.open('w',encoding='utf-8') as out:
 while time.time()-start<420:
  try:line=q.get(timeout=.2)
  except queue.Empty:line=''
  if line:
   out.write(line);out.flush()
   if any(s in line for s in ['Done (','Failed','ERROR','Generated structure','enabled data','Unknown','Exception']):print(line.rstrip(),flush=True)
   if 'Done (' in line:started=True;next_step=time.time()+2
  if started and steps<len(commands) and time.time()>next_step:
   command(commands[steps]);print('COMMAND',commands[steps],flush=True);steps+=1;next_step=time.time()+ (10 if steps==2 else 40 if steps==6 else 3)
  if p.poll() is not None:break
 if p.poll() is None:command('stop');p.wait(timeout=60)
print('EXIT',p.returncode,'COMMANDS',steps,flush=True)
