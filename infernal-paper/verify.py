"""Two real Paper boots with an isolated test plugin; no production server changes."""
import hashlib,json,re,shutil,subprocess,sys,time,zipfile
from pathlib import Path
from build import BASE,ROOT,JAVA,LIBS,JAR
WORK=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else BASE/'test-server'/str(int(time.time()));PLUGINS=WORK/'plugins';PLUGINS.mkdir(parents=True,exist_ok=True)
preferred=ROOT/'.tools/paper263-latest/paper.jar'
SERVERJAR=Path(sys.argv[2]).resolve() if len(sys.argv)>2 else preferred if preferred.exists() else ROOT/'.tools/paper263/paper.jar'
shutil.copy2(JAR,PLUGINS/JAR.name)
cache=WORK/'cache';cache.mkdir(exist_ok=True)
for p in (ROOT/'.tools/paper263/cache').glob('mojang_26.3.jar'):
 if not (cache/p.name).exists():shutil.copy2(p,cache/p.name)
classes=BASE/'build/test-classes';classes.mkdir(parents=True,exist_ok=True)
native_server=ROOT/'.tools/paper263/versions/26.3/paper-26.3.jar'
subprocess.run([str(JAVA/'javac.exe'),'--release','25','-encoding','UTF-8','-cp',';'.join(map(str,[JAR,native_server,*LIBS])),'-d',str(classes),*map(str,(BASE/'test').rglob('*.java'))],check=True)
with zipfile.ZipFile(PLUGINS/'InfernalProbe.jar','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('plugin.yml','name: InfernalProbe\nversion: 1.0\nmain: kr.infernal.test.InfernalProbe\napi-version: \'26.3\'\ndepend: [InfernalDifficulties]\n')
 for p in classes.rglob('*.class'):z.write(p,p.relative_to(classes).as_posix())
(WORK/'eula.txt').write_text('eula=true\n')
(WORK/'server.properties').write_text('\n'.join(['level-name=probe-world','level-type=minecraft:flat','generator-settings={"layers":[{"block":"minecraft:bedrock","height":1},{"block":"minecraft:stone","height":2}],"biome":"minecraft:plains"}','generate-structures=false','online-mode=false','server-ip=127.0.0.1','server-port=25629','view-distance=2','simulation-distance=2','spawn-protection=0','difficulty=hard','max-tick-time=-1'])+'\n')
logs=[]
for phase in (1,2):
 cmd=[str(JAVA/'java.exe'),'-Dterminal.jline=false','-Dterminal.ansi=false','-Djava.net.preferIPv4Stack=true','-Djdk.net.unixdomain.tmpdir=','-Djava.nio.channels.spi.SelectorProvider=sun.nio.ch.WindowsSelectorProvider','-XX:ActiveProcessorCount=4','-Xms256M','-Xmx2G','-jar',str(SERVERJAR),'--nogui']
 try:
  run=subprocess.run(cmd,cwd=WORK,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',timeout=180)
 except subprocess.TimeoutExpired as e:
  (BASE/'output/plugin-validation-timeout.log').write_bytes(e.stdout or b'');raise
 log=run.stdout;logs.append(log)
 (BASE/f'output/plugin-validation-phase{phase}.log').write_text('\n'.join(line.rstrip() for line in log.splitlines())+'\n',encoding='utf-8')
 print(log[-8000:],flush=True)
 assert run.returncode==0 and f'INFERNAL_PHASE{phase}_PASS' in log and 'INFERNAL_TEST_FAIL' not in log,log[-12000:]
result={'paper':re.search(r'This server is running Paper version ([^ ]+)',logs[0]).group(1),'jar_sha256':hashlib.sha256(JAR.read_bytes()).hexdigest(),'phases':[json.loads((WORK/f'phase{p}.json').read_text()) for p in (1,2)],'datapack_required':False}
(BASE/'output/validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('All real Paper integration checks passed.')
