from pathlib import Path
import json, zipfile, re, collections, concurrent.futures, urllib.request, urllib.parse, time, hashlib, gzip, io
import nbtlib

B=Path(__file__).resolve().parent
S=next((B/'source').iterdir())
O=B/'instance-overlay'
R=O/'config/openloader/resources/zz_explorers_eve_ko'
D=O/'config/openloader/data/zz_explorers_eve_ko'
memory=json.loads((B/'memory.json').read_text('utf-8')) if (B/'memory.json').exists() else {}
old=B.parent/'cnw-ko/translation-memory.json'
if old.exists():
 for k,v in json.loads(old.read_text('utf-8')).items(): memory.setdefault(k,v)
manual={"Wither Storm":"위더 스톰", "Withered Symbiont":"위더 공생체", "Explorer's Treasure":"탐험가의 보물", "Explorer's Guide":"탐험가의 안내서", "Explorer's Eve":"Explorer's Eve", "Command Block":"명령 블록", "Super TNT":"슈퍼 TNT", "Formidibomb":"포미디밤", "The Twilight Forest":"황혼의 숲", "The Aether":"에테르", "Blue Skies":"블루 스카이", "Deep Aether":"딥 에테르", "Mr. Stabby":"푹찍이", "Sharpness CCLV":"날카로움 CCLV"}
manual.update({'Item:':'아이템:', 'Prev.':'이전', 'Nyctofly':'닉토플라이', 'Type:':'유형:', 'Cover Me in Sunshine':'햇살로 감싸 줘', '@ModName':'@모드명', '%%CreativeTab':'%%크리에이티브탭', 'Air/Liquid':'공기/액체', 'Occlude Sounds Underground':'지하 소리 차폐', 'Add/Edit':'추가/편집', 'Instructions/Help':'사용법/도움말', 'Centered:':'중앙 정렬:', 'Flipped:':'뒤집기:', 'Disable/Enable':'끄기/켜기', 'World/Server':'월드/서버', 'Sub-World/Dimension':'하위 월드/차원', 'Color:':'색상:', 'Visibility:':'표시 여부:', 'Names:':'이름:', 'Icons/Heads:':'아이콘/머리:', 'Search...':'검색...', 'Category:':'분류:', 'Raining/Snowing':'비/눈', 'BL: %d':'블록 밝기: %d', 'SL: %d':'하늘 밝기: %d', 'BL: %d SL: %d':'블록: %d 하늘: %d', 'yyyy/MM/dd HH:mm:ss':'yyyy/MM/dd HH:mm:ss'})
memory.update(manual)
glossary={'Wither Storm':'위더 스톰','Withered Symbiont':'위더 공생체',"Explorer's Treasure":'탐험가의 보물',"Explorer's Guide":'탐험가의 안내서','Wither Sickness':'위더병','Formidibomb':'포미디밤','Command Block':'명령 블록','Twilight Forest':'황혼의 숲','Deep Aether':'딥 에테르','Aether':'에테르','Blue Skies':'블루 스카이','Zanite':'자나이트','Gravitite':'그라비타이트','Holystone':'신성석','Skyroot':'하늘뿌리나무','Ambrosium':'앰브로슘','Valkyrie':'발키리','Moa':'모아','Sun Spirit':'태양의 정령','Aerogel':'에어로젤'}
GLOSS=re.compile(r'\b(?:'+'|'.join(re.escape(k) for k in sorted(glossary,key=len,reverse=True))+r')\b',re.I)
glower={k.lower():v for k,v in glossary.items()}
refined=set(json.loads((B/'refined.json').read_text('utf-8'))) if (B/'refined.json').exists() else set()
MASK=re.compile(r'\$\([^)]*\)|%(?:\d+\$)?[-#+ 0,(]*\d*(?:\.\d+)?[a-zA-Z%]|§[0-9a-fk-or]|https?://[^\s)]+|\{[0-9]+\}|<NEWLINE>|\n|\\n')
pending=set(); phase='collect'
def tr(s):
 if not isinstance(s,str) or not re.search('[A-Za-z]',s):return s
 if s in manual:return manual[s]
 if re.fullmatch(r'[a-z0-9_]+(?:[.:/][a-z0-9_/-]+)+',s):return s
 if s in {'Gearsaw Studios'}:return s
 if s.startswith('%%'):return s
 if phase=='collect':pending.add(s);return s
 return memory[s]
def dump(d):return json.dumps(d,ensure_ascii=False,indent=2)+'\n'
def write(p,d):
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(d,encoding='utf-8',newline='\n')
def obj(x,book=False):
 if isinstance(x,list):return [obj(v,book) for v in x]
 if isinstance(x,str) and x.lstrip().startswith(('{','[')):
  try:
   d=json.loads(x);new=obj(d)
   return json.dumps(new,ensure_ascii=False,separators=(',',':')) if new!=d else x
  except ValueError:return command(x)
 if not isinstance(x,dict):return x
 out={}
 for k,v in x.items():
  if isinstance(v,str) and (k=='text' or book and k in {'name','description','title','landing_text','subtitle'} or k=='name' and x.get('function') in {'minecraft:set_name','set_name'}):out[k]=tr(v)
  elif isinstance(v,str) and k in {'title','description'} and ('icon' in x or 'frame' in x):out[k]=tr(v)
  elif isinstance(v,str) and v.lstrip().startswith(('{','[')):
   try:out[k]=json.dumps(obj(json.loads(v)),ensure_ascii=False,separators=(',',':'))
   except (ValueError,TypeError):out[k]=command(v)
  else:out[k]=obj(v,book)
 return out

# Rewrite only JSON text component literals, including JSON nested inside SNBT strings.
LEX=re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'')
def dec(t):
 if t[0]=='"':return json.loads(t)
 return re.sub(r"\\([\\'])",r'\1',t[1:-1])
def enc(s,q):return json.dumps(s,ensure_ascii=False) if q=='"' else "'"+s.replace('\\','\\\\').replace("'","\\'")+"'"
def command(t):
 def replace(m):
  raw=m[0]
  try:v=dec(raw)
  except ValueError:return raw
  if v.lstrip().startswith(('{','[')):
   try:
    new=obj(json.loads(v))
    if new!=json.loads(v):return enc(json.dumps(new,ensure_ascii=False,separators=(',',':')),raw[0])
   except ValueError:pass
  prefix=t[max(0,m.start()-30):m.start()]
  if re.search(r'(?:"text"|\btext|\btitle|\bauthor)\s*:\s*$',prefix):return enc(tr(v),raw[0])
  return raw
 return '\n'.join(LEX.sub(replace,line) if not line.lstrip().startswith('#') else line for line in t.split('\n')) if False else LEX.sub(replace,t)

langs={}; sources=[]; books=[]; datajobs=[]; fnjobs=[]; nbtjobs=[]; txtjobs=[]; modnames=[]; native_nbt=[]
overridden=set()
for p in (S/'config/openloader/data').glob('*'):
 if p.is_dir():overridden.update(x.relative_to(p).as_posix() for x in p.rglob('*') if x.is_file())
for p in sorted((S/'mods').glob('*.jar')):
 modnames.append(p.name)
 with zipfile.ZipFile(p) as z:
  ns=set(z.namelist())
  for n in sorted(ns):
   if n.startswith('data/') and n.endswith('.nbt') and n not in overridden:
    raw=z.read(n)
    try:raw=gzip.decompress(raw)
    except OSError:pass
    if b'"text"' in raw:native_nbt.append((n,raw))
   if re.fullmatch(r'assets/[^/]+/(?:lang|blue_skies/journal_lang)/en_us.json',n):
    en=json.loads(z.read(n));kp=n.replace('/en_us.json','/ko_kr.json')
    ko=json.loads(z.read(kp)) if kp in ns else {}
    # Some bundled Korean files still contain English placeholders.
    dest=langs.setdefault(kp,{})
    count=0
    for k,v in en.items():
     existing=ko.get(k)
     if existing and (existing!=v or re.search('[가-힣]',existing)) and collections.Counter(MASK.findall(existing))==collections.Counter(MASK.findall(v)):dest[k]=existing
     else:dest[k]=v;count+=1
    sources.append({'source':p.name,'path':n,'keys':len(en),'requires_translation':count})
   if '/book/' in n and '/en_us/' in n and n.endswith('.txt'):
    txtjobs.append((n.replace('/en_us/','/ko_kr/'),z.read(n).decode('utf-8')))
   if '/patchouli_books/' in n and '/en_us/' in n and n.endswith('.json'):
    books.append((R/n.replace('/en_us/','/ko_kr/'),json.loads(z.read(n))))

# Pack overrides deliberately take precedence over mod defaults, even when a mod has Korean.
for p in sorted((S/'config/openloader/resources').rglob('en_us.json')):
 rel=p.relative_to(next(x for x in p.parents if x.parent==S/'config/openloader/resources'))
 d=json.loads(p.read_text('utf-8-sig'))
 kp=rel.as_posix().replace('/en_us.json','/ko_kr.json')
 langs.setdefault(kp,{}).update(d)
 sources.append({'source':str(p.relative_to(S)),'path':str(rel),'keys':len(d),'requires_translation':len(d)})
for p in (S/'patchouli_books').rglob('*.json'):
 rel=p.relative_to(S)
 dest=O/str(rel).replace('en_us','ko_kr')
 books.append((dest,json.loads(p.read_text('utf-8-sig'))))
for p in (S/'config/openloader/data').rglob('*.json'):
 try:datajobs.append((p,json.loads(p.read_text('utf-8-sig'))))
 except ValueError:pass
for p in (S/'config/openloader/data').rglob('*.mcfunction'):
 fnjobs.append((p,p.read_text('utf-8-sig')))
for p in (S/'config/openloader/data').rglob('*.nbt'):
 raw=p.read_bytes()
 try:raw=gzip.decompress(raw)
 except OSError:pass
 if b'"text"' in raw:nbtjobs.append(p)

def nbtwalk(v):
 global nbtchanges
 if isinstance(v,nbtlib.String):
  text=str(v)
  if text.lstrip().startswith(('{','[')):
   try:
    d=json.loads(text);new=obj(d)
    if new!=d:
     nbtchanges+=1
     return nbtlib.String(json.dumps(new,ensure_ascii=False,separators=(',',':')))
   except ValueError:pass
  return v
 if isinstance(v,(dict,nbtlib.Compound)):
  for k in list(v):v[k]=nbtwalk(v[k])
 elif isinstance(v,(list,nbtlib.List)):
  for i in range(len(v)):v[i]=nbtwalk(v[i])
 return v

def process():
 counts=collections.Counter()
 for path,d in langs.items():
  # Translate English fallback only; preserve existing Korean.
  out={k:tr(v) if not re.search('[가-힣]',v) else v for k,v in d.items()}
  if phase=='write':write(R/path,dump(out))
  counts['language_keys']+=len(d)
 for p,d in books:
  out=obj(d,True)
  if phase=='write':write(p,dump(out))
  counts['guidebook_files']+=1
 for p,d in datajobs:
  out=obj(d)
  if out!=d and phase=='write':write(O/p.relative_to(S),dump(out));counts['data_json_files']+=1
 for p,t in fnjobs:
  # Keep comments and all command syntax untouched.
  out='\n'.join(line if line.lstrip().startswith('#') else command(line) for line in t.split('\n'))
  if out!=t and phase=='write':write(O/p.relative_to(S),out);counts['function_files']+=1
 global nbtchanges
 for p in nbtjobs:
  n=nbtlib.load(p);nbtchanges=0;nbtwalk(n)
  if nbtchanges and phase=='write':
   dest=O/p.relative_to(S);dest.parent.mkdir(parents=True,exist_ok=True);n.save(dest);counts['structure_files']+=1
 for path,raw in native_nbt:
  n=nbtlib.File.parse(io.BytesIO(raw));nbtchanges=0;nbtwalk(n)
  if nbtchanges and phase=='write':
   dest=D/path;dest.parent.mkdir(parents=True,exist_ok=True);n.save(dest,gzipped=True);counts['native_structure_files']+=1
 for path,t in txtjobs:
  out='\n\n'.join(tr(block) for block in re.split(r'\r?\n\s*\r?\n',t))
  if phase=='write':write(R/path,out)
  counts['citadel_pages']+=1
 return counts

process()
todo=sorted(s for s in pending if s not in memory or collections.Counter(MASK.findall(s))!=collections.Counter(MASK.findall(memory[s])) or s not in refined and (GLOSS.search(s) or '$(' in s))
print('Pending unique strings:',len(pending),'new:',len(todo),flush=True)
write(B/'pending.json',dump(todo))
def fetch(batch):
 masked=[];tokens=[]
 for text in batch:
  tok=[]
  def mask(m):tok.append(m[0]);return f'ZXQ{len(tok)-1}QXZ'
  text=GLOSS.sub(lambda m:glower[m[0].lower()],text)
  masked.append(MASK.sub(lambda m:' '+mask(m)+' ',text));tokens.append(tok)
 query=[('client','dict-chrome-ex'),('sl','en'),('tl','ko')]+[('q',s) for s in masked]
 url='https://clients5.google.com/translate_a/t?'+urllib.parse.urlencode(query)
 for attempt in range(3):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
   data=json.load(urllib.request.urlopen(req,timeout=50))
   if len(data)!=len(batch) or not all(isinstance(v,str) for v in data):raise ValueError('Bad response')
   result={}
   for source,v,tok in zip(batch,data,tokens):
    for i,token in enumerate(tok):
     pattern=re.compile(r'ZXQ\s*'+str(i)+r'\s*QXZ',re.I)
     if len(pattern.findall(v))!=1:raise ValueError('Placeholder lost')
     v=pattern.sub(lambda m:token,v)
    if collections.Counter(MASK.findall(source))!=collections.Counter(MASK.findall(v)):raise ValueError('Formatting changed')
    result[source]=v
   return result
  except Exception:
   if attempt==2:
    if len(batch)>1:
     mid=len(batch)//2;return fetch(batch[:mid])|fetch(batch[mid:])
    pieces=re.split('('+MASK.pattern+')',batch[0])
    plain=[p.strip() for p in pieces if p.strip() and not MASK.fullmatch(p) and re.search('[A-Za-z]',p)]
    if len(pieces)>1 and plain:
     print('Retrying protected segments:',repr(batch[0][:70]),flush=True)
     translated=fetch(list(dict.fromkeys(plain)))
     return {batch[0]:''.join((p[:len(p)-len(p.lstrip())]+translated[p.strip()]+p[len(p.rstrip()):]) if p.strip() in translated else p for p in pieces)}
    print('Translation error:',repr(batch[0]),flush=True)
    raise
   time.sleep(attempt+1)
batches=[];batch=[];size=0
for s in todo:
 if batch and (size+len(urllib.parse.quote(s))>4500 or len(batch)>=25):batches.append(batch);batch=[];size=0
 batch.append(s);size+=len(urllib.parse.quote(s))
if batch:batches.append(batch)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 futures=[pool.submit(fetch,b) for b in batches]
 for i,f in enumerate(concurrent.futures.as_completed(futures),1):
  memory.update(f.result())
  write(B/'memory.json',dump(memory))
  refined.update(f.result())
  write(B/'refined.json',dump(sorted(refined)))
  if i%10==0 or i==len(futures):print('Translation batches',i,'/',len(futures),flush=True)
phase='write'
counts=process()
write(R/'pack.mcmeta',dump({'pack':{'pack_format':13,'description':'Explorer’s Eve 전체 한국어 번역 — 모드·안내서·팩 전용 문구'}}))
write(D/'pack.mcmeta',dump({'pack':{'pack_format':12,'description':'Explorer’s Eve 한국어 구조물 문구'}}))
report={'minecraft':'1.19.4','mods_scanned':len(modnames),'language_files':len(langs),'unique_strings':len(pending),'counts':dict(counts),'sources':sources,'mods':modnames}
write(B/'coverage.json',dump(report))
print(dump(report['counts']),flush=True)
