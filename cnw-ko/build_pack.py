import concurrent.futures, hashlib, io, json, re, time, urllib.parse, urllib.request, zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parent
SOURCE = Path(r'C:/Users/user/curseforge/minecraft/Instances/Create New World  A Locked Progression Experience.zip')
OUT = BASE / 'instance-overlay'
CACHE = BASE / 'translation-memory.json'
STR = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'')
JSLEX = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|'+STR.pattern)
TOKEN = re.compile(r'(\{[^{}]*\}|https?://[^\s]+|[§&][0-9a-fk-or]|%(?:\d+\$)?[sdif]|\n|\\n)', re.I)
memory = json.loads(CACHE.read_text('utf-8')) if CACHE.exists() else {}
manual = {'Milestone': '이정표', 'Milestones': '이정표', 'Research': '연구', 'Reserch Complete!': '연구 완료!', 'MILESTONE UNLOCKED': '이정표 해금', 'New Milestones are now available': '새로운 이정표를 진행할 수 있습니다', 'Basic Machinery': '기초 기계', 'Contraptions': '움직이는 장치', 'Copycat Blocks': '모방 블록', 'Disabled': '사용 불가', 'Fragmented Ender Eye': '파편화된 엔더의 눈', 'Item Sink': '아이템 소각기', 'Solo': '싱글플레이', 'Servers': '서버', 'Settings': '설정', 'Progression Recovered!': '진행 상황 복구 완료!', 'Temperature': '온도', 'Survival': '생존', 'Discovery': '탐험', 'Economy': '경제', 'Hidden Messages': '숨겨진 메시지', 'Introductions': '시작 안내', 'Research (WIP)': '연구 (개발 중)', 'Rotational Power Generation': '회전 동력 생산', 'Rotational Power Transportation': '회전 동력 전달', 'Advanced Processing': '고급 가공', 'Super Heating': '초고열 가열', 'Schematics': '설계도', 'Fluids': '유체', 'Logistics': '물류', 'Copper Diving Equipment': '구리 잠수 장비', 'Incomplete': '미완성', 'test': '테스트'}
for i in range(1, 11): manual[f'Stage {i} Unlocked'] = f'{i}단계 해금'
memory.update(manual)
overrides=json.loads((BASE/'manual-overrides.json').read_text('utf-8')) if (BASE/'manual-overrides.json').exists() else {}
memory.update(overrides)

def decode(s):
    if s.startswith('"'): return json.loads(s)
    return re.sub(r'\\([\\\'"nrt])', lambda m: {'n':'\n','r':'\r','t':'\t'}.get(m[1],m[1]), s[1:-1])

def parts(s): return TOKEN.split(s)
def eligible(s): return bool(re.search('[A-Za-z]', s)) and not TOKEN.fullmatch(s) and not re.fullmatch(r'[\s\W\d_]+',s)
def units(s): return [p.strip() for p in parts(s) if eligible(p)]
pending = set()
def collect(s): pending.update(x for x in units(s) if x not in memory)
def translate(s):
    if s in overrides:return overrides[s]
    def one(p):
        if not eligible(p): return p
        c=p.strip(); return p[:len(p)-len(p.lstrip())] + memory.get(c,c) + p[len(p.rstrip()):]
    return ''.join(one(p) for p in parts(s))

def fetch(batch):
    query=[('client','dict-chrome-ex'),('sl','en'),('tl','ko')]+[('q',x) for x in batch]
    url='https://clients5.google.com/translate_a/t?'+urllib.parse.urlencode(query)
    for attempt in range(5):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
            data=json.load(urllib.request.urlopen(req,timeout=45))
            if len(data)!=len(batch) or not all(isinstance(x,str) for x in data): raise ValueError('unexpected translation response')
            return dict(zip(batch,data))
        except Exception:
            if attempt==4: raise
            time.sleep(2*(attempt+1))

def write(rel,data):
    p=OUT/rel;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(data,encoding='utf-8',newline='\n')
def dump(d):return json.dumps(d,ensure_ascii=False,indent=2)+'\n'

with zipfile.ZipFile(SOURCE) as z:
    root=z.namelist()[0].split('/')[0]+'/'
    def read(r):return z.read(root+r).decode('utf-8-sig').replace('\r\n','\n').replace('\r','')
    jobs=[]
    quest=read('config/ftbquests/quests/lang/en_us.snbt')
    for m in STR.finditer(quest): collect(decode(m[0]))
    jobs.append(('snbt','config/ftbquests/quests/lang/ko_kr.snbt',quest,None))
    for r in ['kubejs/assets/cnw/lang/en_us.json','kubejs/assets/collapsible_groups/lang/en_us.json','kubejs/assets/collapsible_groups/group_lang/en_us.json','config/collapsiblegroups/lang/en_us.json']:
        d=json.loads(read(r))
        for v in d.values(): collect(v)
        jobs.append(('json',r.replace('en_us.json','ko_kr.json'),d,None))
    scripts=['kubejs/client_scripts/tooltips.js','kubejs/server_scripts/jei.js','kubejs/server_scripts/stages.js','kubejs/server_scripts/stage_recovery.js','kubejs/server_scripts/custom_commands.js','kubejs/server_scripts/server_rules.js','kubejs/server_scripts/item_oblitorator.js','kubejs/startup_scripts/items_registry.js']
    for r in scripts:
        t=read(r); positions={}
        for m in JSLEX.finditer(t):
            if m[0].startswith(('//','/*')):continue
            value=decode(m[0]);line=t[t.rfind('\n',0,m.start())+1:m.start()]
            if line.lstrip().startswith('//'):continue
            visible=bool(re.search(r'\s',value) and not value.startswith(('[STAGE RECOVERY]', 'cnw_'))) or value=='Disabled'
            if visible:
                positions[m.start()]=value;collect(value)
        jobs.append(('js',r,t,positions))
    r='config/ftbquests/quests/chapters/introductions.snbt';t=read(r);positions={}
    for m in STR.finditer(t):
        if re.search(r'description:\s*$',t[max(0,m.start()-30):m.start()]):positions[m.start()]=decode(m[0]);collect(decode(m[0]))
    jobs.append(('js',r,t,positions))
    # Generated names for pack-specific registry entries.
    custom={}
    for kind,r in [('item','kubejs/startup_scripts/items_registry.js'),('block','kubejs/startup_scripts/blocks_registry.js')]:
        for ident in re.findall(r'event\.create\([\'"]([^\'"]+)',read(r)):
            ns,name=ident.split(':',1) if ':' in ident else ('kubejs',ident)
            value='Fragmented Ender Eye' if name=='ender_eye' else name.replace('_',' ').title()
            if name.startswith('item_sink'):value='Item Sink'+(' (Powered)' if name.endswith('powered') else '')
            custom[f'{kind}.{ns}.{name}']=value;collect(value)
    jobs.append(('json','kubejs/assets/kubejs/lang/ko_kr.json',custom,None))
    jobs.append(('json','kubejs/assets/custommachinery/lang/ko_kr.json',{'block.custommachinery.item_sink':'Item Sink'},None))
    collect('Item Sink')
    jobs.append(('json','kubejs/assets/minecraft/lang/ko_kr.json',{'Item Sink':'Item Sink'},None))
    # High-priority progression mods; keep all existing Korean entries untouched.
    priority={'northstar','ftbquests','create_aeronautics_automated_logistics','create_enchantment_industry','custommachinery','createbigcannons','createdieselgenerators','createpropulsion','createqol','block_factorys_bosses'}
    mod_report=[]
    for n in z.namelist():
        if '/mods/' not in n or not n.endswith('.jar'):continue
        with zipfile.ZipFile(io.BytesIO(z.read(n))) as jar:
            names=set(jar.namelist())
            for enpath in sorted(names):
                match=re.fullmatch(r'assets/([^/]+)/lang/en_us.json',enpath)
                if not match:continue
                ns=match[1]
                try:
                    en=json.loads(jar.read(enpath));kp=enpath.replace('en_us.json','ko_kr.json');ko=json.loads(jar.read(kp)) if kp in names else {}
                except (ValueError,UnicodeDecodeError):continue
                missing={k:v for k,v in en.items() if k not in ko and isinstance(v,str)}
                mod_report.append({'namespace':ns,'jar':n.split('/')[-1],'english_keys':len(en),'missing_keys':len(missing),'included':ns in priority})
                if ns in priority:
                    for v in missing.values():collect(v)
                    jobs.append(('json',f'kubejs/assets/{ns}/lang/ko_kr.json',missing,None))
    print('Translation units:',len(pending),flush=True)
    batches=[];batch=[];length=0
    for s in sorted(pending):
        cost=len(urllib.parse.quote(s))+4
        if batch and (length+cost>5500 or len(batch)>=24):batches.append(batch);batch=[];length=0
        batch.append(s);length+=cost
    if batch:batches.append(batch)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for i,result in enumerate(pool.map(fetch,batches),1):
            memory.update(result)
            CACHE.write_text(dump(memory),encoding='utf-8')
            if i%10==0 or i==len(batches):print(f'Translated batches {i}/{len(batches)}',flush=True)
    changes=[]
    for kind,r,data,positions in jobs:
        if kind=='json':
            prior=json.loads((OUT/r).read_text('utf-8')) if (OUT/r).exists() else {}
            prior.update({k:translate(v) for k,v in data.items()})
            output=dump(prior)
            count=len(data)
        else:
            def replacement(m):
                if m[0].startswith(('//','/*')):return m[0]
                if kind=='snbt' or m.start() in positions:return json.dumps(translate(decode(m[0])),ensure_ascii=False)
                return m[0]
            lexer=STR if kind=='snbt' or r.endswith('.snbt') else JSLEX
            output=lexer.sub(replacement,data)
            count=len(STR.findall(data)) if kind=='snbt' else len(positions)
            # Same program / SNBT structure, with only string values changed.
            skeleton=lambda t:lexer.sub(lambda m:m[0] if m[0].startswith(('//','/*')) else '"S"',t)
            assert skeleton(data)==skeleton(output),r
            for old,new in zip(lexer.finditer(data),lexer.finditer(output)):
                if old[0]!=new[0]:assert TOKEN.findall(decode(old[0]))==TOKEN.findall(decode(new[0])),r
        write(r,output);changes.append({'path':r,'entries':count})
    write('resourcepacks/CNW-Korean/pack.mcmeta',dump({'pack':{'pack_format':34,'description':'Create New World 4.0.12 한국어 번역 초안'}}))
    # A resource pack can be used alone for menus, mod UI and generated names.
    resource=BASE/'CNW-Korean-Resources-4.0.12.zip'
    with zipfile.ZipFile(resource,'w',zipfile.ZIP_DEFLATED) as pack:
        pack.writestr('pack.mcmeta',json.dumps({'pack':{'pack_format':34,'description':'Create New World 4.0.12 한국어 번역 초안'}},ensure_ascii=False))
        for p in (OUT/'kubejs/assets').rglob('ko_kr.json'):pack.write(p,'assets/'+p.relative_to(OUT/'kubejs/assets').as_posix())
    # Avoid shipping an empty resource-pack folder in the overlay.
    (OUT/'resourcepacks/CNW-Korean/pack.mcmeta').unlink()
    (OUT/'resourcepacks/CNW-Korean').rmdir();(OUT/'resourcepacks').rmdir()
    audit={'source':str(SOURCE),'source_version':'4.0.12','minecraft':'1.21.1','translation':'Google Translate machine translation with a small manually curated glossary; in-game review required','files':changes,'mods':mod_report,'validation':{'string_structure_preserved':True,'format_tokens_preserved':True,'in_game_tested':False}}
    (BASE/'coverage.json').write_text(dump(audit),encoding='utf-8')
    print('DONE',len(changes),'files',flush=True)
