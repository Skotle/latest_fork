from pathlib import Path
import json,re,zipfile,collections,hashlib,gzip,io
import nbtlib
B=Path(__file__).resolve().parent;S=next((B/'source').iterdir());O=B/'instance-overlay';R=O/'config/openloader/resources/zz_explorers_eve_ko'
errors=[];checks=collections.Counter()
def require(ok,msg):
 if not ok:errors.append(msg)
def normalize(x):
 if isinstance(x,dict):return {k:('<visible>' if k=='text' and isinstance(v,str) else normalize(v)) for k,v in x.items()}
 if isinstance(x,list):return [normalize(v) for v in x]
 return x
LEX=re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'')
def decode(t):
 return json.loads(t) if t[0]=='"' else re.sub(r"\\([\\'])",r'\1',t[1:-1])
def cmdshape(t):
 if '\n' in t:return '\n'.join(line if line.lstrip().startswith('#') else cmdshape(line) for line in t.split('\n'))
 def f(m):
  try:v=decode(m[0])
  except ValueError:return m[0]
  if v.lstrip().startswith(('{','[')):
   try:return json.dumps(normalize(json.loads(v)),sort_keys=True)
   except ValueError:pass
  if re.search(r'(?:"text"|\btext|\btitle|\bauthor)\s*:\s*$',t[max(0,m.start()-30):m.start()]):return '"<visible>"'
  return m[0]
 return LEX.sub(f,t)
def jsonshape(x,parent=None):
 if isinstance(x,list):return [jsonshape(v,parent) for v in x]
 if isinstance(x,str) and x.lstrip().startswith(('{','[')):
  try:return normalize(json.loads(x))
  except ValueError:return cmdshape(x)
 if not isinstance(x,dict):return x
 out={}
 for k,v in x.items():
  if isinstance(v,str) and (k=='text' or k in {'title','description'} and ('icon' in x or 'frame' in x) or k=='name' and x.get('function') in {'minecraft:set_name','set_name'}):out[k]='<visible>'
  else:out[k]=jsonshape(v,k)
 return out
for p in O.rglob('*'):
 if p.is_file() and p.suffix in {'.json','.mcmeta'}:
  try:json.loads(p.read_text('utf-8'));checks['valid_json']+=1
  except Exception as e:errors.append(f'{p}: {e}')
for p in (O/'config/openloader/data').rglob('*.json'):
 source=S/p.relative_to(O)
 if source.exists():
  a=json.loads(source.read_text('utf-8-sig'));b=json.loads(p.read_text('utf-8'))
  require(jsonshape(a)==jsonshape(b),f'Data semantics: {p}');checks['data_structure_preserved']+=1
for p in O.rglob('*.mcfunction'):
 a=(S/p.relative_to(O)).read_text('utf-8-sig');b=p.read_text('utf-8')
 require(cmdshape(a)==cmdshape(b),f'Command syntax changed: {p}');checks['command_files_preserved']+=1
def nbt_digest(value):
 h=hashlib.sha256()
 def walk(v):
  h.update(type(v).__name__.encode())
  if isinstance(v,(dict,nbtlib.Compound)):
   for k in sorted(v):h.update(k.encode());walk(v[k])
  elif isinstance(v,(list,nbtlib.List)):
   for child in v:walk(child)
  elif isinstance(v,nbtlib.String):
   try:h.update(json.dumps(normalize(json.loads(str(v))),sort_keys=True).encode())
   except ValueError:h.update(str(v).encode())
  elif hasattr(v,'tobytes'):h.update(v.tobytes())
  else:h.update(str(v).encode())
 walk(value);return h.digest()
for p in O.rglob('*.nbt'):
 source=S/p.relative_to(O)
 if source.exists():original=nbtlib.load(source)
 else:
  rel=p.relative_to(O/'config/openloader/data/zz_explorers_eve_ko').as_posix();original=None
  for jar in (S/'mods').glob('*.jar'):
   with zipfile.ZipFile(jar) as z:
    if rel in z.namelist():
     raw=z.read(rel)
     try:raw=gzip.decompress(raw)
     except OSError:pass
     original=nbtlib.File.parse(io.BytesIO(raw));break
 require(original is not None and nbt_digest(original)==nbt_digest(nbtlib.load(p)),f'NBT structure changed: {p}')
 checks['structure_data_preserved']+=1
report=json.loads((B/'coverage.json').read_text('utf-8'))
for row in report['sources']:
 path=row['path'].replace('\\','/').replace('/en_us.json','/ko_kr.json')
 p=R/path;require(p.exists(),f'Missing language: {path}')
 if not p.exists():continue
 dest=json.loads(p.read_text('utf-8'))
 if row['source'].endswith('.jar'):
  with zipfile.ZipFile(S/'mods'/row['source']) as z:en=json.loads(z.read(row['path']))
 else:en=json.loads((S/row['source']).read_text('utf-8-sig'))
 require(set(en)<=set(dest),f'Missing keys: {path}')
 checks['language_sources_covered']+=1
# Check effective mod and pack language values, not superseded English defaults.
effective={}
for row in report['sources']:
 path=row['path'].replace('\\','/')
 if row['source'].endswith('.jar'):
  with zipfile.ZipFile(S/'mods'/row['source']) as z:d=json.loads(z.read(row['path']))
 else:d=json.loads((S/row['source']).read_text('utf-8-sig'))
 effective.setdefault(path,{}).update(d)
TOKEN=re.compile(r'\$\([^)]*\)|%(?:\d+\$)?[-#+ 0,(]*\d*(?:\.\d+)?[a-zA-Z%]|§[0-9a-fk-or]|https?://[^\s)]+|\{[0-9]+\}|<NEWLINE>|\n|\\n')
for path,en in effective.items():
 ko=json.loads((R/path.replace('/en_us.json','/ko_kr.json')).read_text('utf-8'))
 for key,v in en.items():
  # Existing bundled Korean has its own historical formatting; report only generated strings.
  mem=json.loads((B/'memory.json').read_text('utf-8')) if False else None
  if TOKEN.search(v):require(collections.Counter(TOKEN.findall(v))==collections.Counter(TOKEN.findall(ko[key])),f'Formatting: {path} {key}')
  checks['effective_language_keys']+=1
for p in (S/'patchouli_books').rglob('en_us/**/*.json'):
 dest=O/str(p.relative_to(S)).replace('en_us','ko_kr')
 require(dest.exists(),f'Guidebook missing: {p}');checks['guidebook_pages_covered']+=1
result={'passed':not errors,'checks':dict(checks),'errors':errors,'runtime_tested':False}
(B/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)

readme='''Explorer’s Eve 한국어 번역팩 (Minecraft 1.19.4 / Forge 45.3.0)

설치
1. 게임을 완전히 종료하고 기존 인스턴스를 백업합니다.
2. ExplorerEve-Korean-Full.zip을 풉니다.
3. 안의 config, patchouli_books 폴더를 모드팩 인스턴스 폴더에 합쳐 넣고 같은 이름의 파일을 덮어씁니다.
   mods 폴더와 같은 위치입니다. 이 ZIP을 resourcepacks 폴더에 그대로 넣으면 안 됩니다.
4. 게임을 재시작하고 언어를 한국어(대한민국)로 설정합니다.
   포함된 OpenLoader가 번역 리소스와 구조물 데이터팩을 자동으로 불러옵니다.

리소스 전용 ZIP
ExplorerEve-Korean-Resources.zip은 선택 사항입니다. resourcepacks 폴더에 넣고 최상단에 활성화할 수 있습니다.
모드의 이름·설정·자막·일지 번역만 필요할 때 쓰며, 안내서·명령어·전리품·구조물 전체 적용에는 Full 설치가 필요합니다.

범위와 주의점
동봉된 coverage.json에 모드별 언어 파일과 처리 수량, verification.json에 정적 검증 결과를 기록했습니다.
기존 한국어 번역을 우선 보존하고 누락 항목은 기계 번역을 보충했으며 주요 고유명사를 통일했습니다.
새로 생성되는 아이템·구조물과 다시 실행되는 메시지에 적용됩니다. 이미 저장된 아이템 이름·책·표지판은 영어가 남을 수 있습니다.
데이터팩의 고정 문구와 안내서 첫 화면은 한국어로 바뀌므로 다른 언어를 쓰는 플레이어도 해당 문구를 한국어로 봅니다.
JAR 안의 하드코딩된 화면 문구, 이미지에 그려진 글자, 외부 모드가 실행 중 생성하는 문구까지 완전 번역했다고 보장하지 않습니다.
실제 게임 실행 검증은 하지 않았습니다. 새 월드에서 안내서, 보스전 안내, 전리품 이름을 확인하는 것을 권장합니다.
모드 JAR 및 세이브 파일은 이 배포본에 포함하지 않습니다. 되돌릴 때는 백업한 파일을 복원합니다.
'''
(B/'README.ko.txt').write_text(readme,'utf-8-sig')
for name,root in [('ExplorerEve-Korean-Full.zip',O),('ExplorerEve-Korean-Resources.zip',R)]:
 with zipfile.ZipFile(B/name,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(root.rglob('*')):
   if p.is_file():z.write(p,p.relative_to(root).as_posix())
  if root==O:
   for n in ['README.ko.txt','coverage.json','verification.json']:z.write(B/n,n)
 with zipfile.ZipFile(B/name) as z:require(z.testzip() is None,f'ZIP CRC failed: {name}')
print('Packaged successfully')
