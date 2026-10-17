"""Compile against the local Paper 26.3 API. Python stdlib + JDK 25 only."""
import hashlib,json,subprocess,zipfile
from pathlib import Path
BASE=Path(__file__).resolve().parent;ROOT=BASE.parent
JAVA=ROOT/'.tools/jdk25/jdk-25.0.4.1+1/bin'
LIBS=list((ROOT/'.tools/paper263/libraries').rglob('*.jar'))
CLASSES=BASE/'build/classes';CLASSES.mkdir(parents=True,exist_ok=True)
subprocess.run([str(JAVA/'javac.exe'),'--release','25','-encoding','UTF-8','-cp',';'.join(map(str,LIBS)),'-d',str(CLASSES),*map(str,(BASE/'src/main/java').rglob('*.java'))],check=True)
OUT=BASE/'output';OUT.mkdir(exist_ok=True)
JAR=OUT/'InfernalDifficulties-1.0.0-Paper-26.3.jar'
with zipfile.ZipFile(JAR,'w',zipfile.ZIP_DEFLATED) as z:
 for source in [CLASSES,BASE/'src/main/resources']:
  for p in sorted(source.rglob('*')):
   if p.is_file():z.write(p,p.relative_to(source).as_posix())
(OUT/'SHA256.json').write_text(json.dumps({JAR.name:hashlib.sha256(JAR.read_bytes()).hexdigest()},indent=2)+'\n')
print(JAR)
