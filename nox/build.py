"""Build a standalone Java 26.3 encounter and an additive resource-pack bundle."""
import hashlib, json, math, re, struct, zipfile, zlib
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
DP = BASE/'datapack'
RP = BASE/'resources'
OUT = BASE/'output'
NS = 'eclipse_nox'

def js(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def fn(name, lines):
    p = DP/f'data/{NS}/function/{name}.mcfunction'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('\n'.join(lines)+'\n', encoding='utf-8')

def call(name): return f'function {NS}:{name}'
def at(name): return f'execute as @e[tag=nox.anchor,tag=nox.current,limit=1] at @s run {call(name)}'
def msg(text): return 'tellraw @a[tag=nox.member] '+json.dumps({'text':text,'color':'gold'},ensure_ascii=False)
def display(name, pos, scale=(1,1,1), tags=()):
    data={'Tags':['nox.owned','nox.visual','nox.'+name,*tags], 'Invulnerable':True,
          'item':{'id':'minecraft:paper','count':1,'components':{'minecraft:item_model':f'{NS}:{name}'}},
          'item_display':'fixed','view_range':2.0,'teleport_duration':1,'interpolation_duration':5,
          'brightness':{'block':12,'sky':12},
          'transformation':{'translation':list(pos),'scale':list(scale),'left_rotation':[0,0,0,1],'right_rotation':[0,0,0,1]}}
    # JSON is also SNBT for these fields.
    return 'summon minecraft:item_display ~ ~ ~ '+json.dumps(data,separators=(',',':'))

def resources():
    js(RP/'pack.mcmeta',{'pack':{'min_format':[97,1],'max_format':[97,1],'description':'Nox additional assets — Java 26.3'}})
    colors=['242337','827657','d7c68b','95e4ee']
    pixels=bytearray()
    for y in range(16):
        pixels.extend(b'\0')
        for x in range(64):
            rgb=bytes.fromhex(colors[x//16]); d=12 if (x+y)%7==0 else -12 if x%16 in (0,15) or y in (0,15) else 0
            pixels.extend([max(0,min(255,c+d)) for c in rgb]+[255])
    def chunk(t,b): return struct.pack('>I',len(b))+t+b+struct.pack('>I',zlib.crc32(t+b)&0xffffffff)
    p=RP/f'assets/{NS}/textures/entity/nox.png';p.parent.mkdir(parents=True,exist_ok=True)
    p.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',64,16,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(pixels))+chunk(b'IEND',b''))
    def box(center,size,mat=0):
        return {'from':[8+c-s/2 for c,s in zip(center,size)],'to':[8+c+s/2 for c,s in zip(center,size)],
                'faces':{f:{'texture':'#atlas','uv':[mat*4,0,mat*4+4,16]} for f in ['up','down','north','south','east','west']}}
    body=[box((0,0,0),(13,14,8)),box((0,9,0),(8,7,8)),box((-9,1,0),(5,13,6),1),box((9,3,0),(5,8,6),1),box((-4,-11,0),(5,9,6)),box((4,-11,0),(5,9,6)),box((0,9,-4.2),(6,1,1),3)]
    core=[box((0,0,0),(4,4,2),3)]
    ring=[box((math.cos(a)*8,math.sin(a)*8,0),(2.5,2.5,2),2) for a in [i*math.tau/16 for i in range(16)]]
    bell=[box((0,5,0),(3,4,3),2),box((0,0,0),(9,7,9),1),box((0,-4,0),(12,2,12),2),box((0,-6,0),(2,3,2),3)]
    sigil=[box((math.cos(a)*7,0,math.sin(a)*7),(2,.25,2),3) for a in [i*math.tau/12 for i in range(12)]]
    models={'body':body,'core':core,'crown':ring,'bell':bell,'sigil':sigil,'relic':ring+core,'device':bell}
    for name,elements in models.items():
        js(RP/f'assets/{NS}/models/{name}.json',{'textures':{'atlas':f'{NS}:entity/nox','particle':f'{NS}:entity/nox'},'elements':elements,'display':{'fixed':{'rotation':[0,0,0],'translation':[0,0,0],'scale':[1,1,1]}}})
        js(RP/f'assets/{NS}/items/{name}.json',{'model':{'type':'minecraft:model','model':f'{NS}:{name}'}})
    js(RP/'assets/minecraft/atlases/items.json',{'sources':[{'type':'minecraft:single','resource':f'{NS}:entity/nox','sprite':f'{NS}:entity/nox'}]})
    # Dedicated event names reuse shipped audio, keeping the bundle redistributable.
    sounds={'bell_low':'block.bell.use','bell_high':'block.bell.resonate','warning':'block.amethyst_block.chime','impact':'entity.warden.sonic_boom','expose':'block.beacon.activate','victory':'ui.toast.challenge_complete'}
    js(RP/f'assets/{NS}/sounds.json',{k:{'sounds':[{'name':'minecraft:'+v,'type':'event'}]} for k,v in sounds.items()})
    js(RP/f'assets/{NS}/lang/ko_kr.json',{'item.eclipse_nox.relic':'일식의 심장','boss.eclipse_nox.name':'일식의 종지기, 녹스'})

def build():
    resources()
    js(DP/'pack.mcmeta',{'pack':{'min_format':[121,0],'max_format':[121,0],'description':'일식의 종지기 녹스 — 독립 보스팩 / Java 26.3'}})
    for name in ['load','tick']: js(DP/f'data/minecraft/tags/function/{name}.json',{'values':[f'{NS}:{name}']})
    objectives=['state','time','phase','hp','max','skill','cast','idle','step','last','lock','puzzle','safe','angle','death','olddeath','leave','oldleave','tmp','next','grace','dx','dz','forward','side']
    load=[f'scoreboard objectives add nx.{o} dummy' for o in objectives if o not in ('death','leave')]
    load += ['scoreboard objectives add nx.death deathCount','scoreboard objectives add nx.leave minecraft.custom:minecraft.leave_game',
             'bossbar add eclipse_nox:health {"text":"일식의 종지기, 녹스","color":"gold"}',
             'bossbar set eclipse_nox:health color purple','bossbar set eclipse_nox:health style notched_20',
             'execute unless score #state nx.state matches 0.. run scoreboard players set #state nx.state 0',
             'execute unless score #installed nx.state matches 0.. run scoreboard players set #installed nx.state 0',
             'execute if score #state nx.state matches 1 run '+call('admin/abort'),
             'tellraw @a {"text":"[녹스] 로드 완료. 설치: /function eclipse_nox:admin/install (주변 지형 덮어쓰기)","color":"gray"}']
    fn('load',load)
    fn('admin/install',['execute unless dimension minecraft:overworld run tellraw @s {"text":"경기장은 오버월드에서만 설치할 수 있습니다.","color":"yellow"}',
                        'execute if score #installed nx.state matches 1 run tellraw @s {"text":"녹스 경기장은 한 월드에 하나만 설치할 수 있습니다. 기존 경기장을 제거하려면 admin/unregister를 사용하세요.","color":"yellow"}',
                        'execute if dimension minecraft:overworld if score #installed nx.state matches 0 positioned ~ ~ ~ align xyz run '+call('arena/install')])
    lines=['scoreboard players set #installed nx.state 1','scoreboard players set #state nx.state 0',
           'summon minecraft:marker ~ ~ ~ {Tags:["nox.owned","nox.anchor"]}']
    # 49-block circular arena, clear headroom only within its footprint.
    for x in range(-24,25):
        zmax=int(math.sqrt(24.5**2-x*x))
        lines += [f'fill ~{x} ~0 ~{-zmax} ~{x} ~16 ~{zmax} minecraft:air',f'fill ~{x} ~-2 ~{-zmax} ~{x} ~-1 ~{zmax} minecraft:polished_deepslate']
        for z in range(-zmax,zmax+1):
            r=math.hypot(x,z)
            block='chiseled_deepslate' if any(abs(r-v)<.45 for v in (7,17,23)) else 'polished_blackstone' if (x+z)%2 else 'deepslate_tiles'
            lines.append(f'setblock ~{x} ~-1 ~{z} minecraft:{block}')
            if r>23.3: lines.append(f'fill ~{x} ~0 ~{z} ~{x} ~3 ~{z} minecraft:tinted_glass')
    lines += ['fill ~-4 ~0 ~23 ~4 ~4 ~24 minecraft:air',
              'fill ~-5 ~-2 ~24 ~5 ~-1 ~34 minecraft:polished_deepslate',
              'fill ~-5 ~0 ~25 ~-5 ~4 ~34 minecraft:polished_blackstone_bricks',
              'fill ~5 ~0 ~25 ~5 ~4 ~34 minecraft:polished_blackstone_bricks',
              'fill ~-5 ~4 ~25 ~5 ~4 ~34 minecraft:polished_blackstone_bricks',
              'fill ~-4 ~0 ~34 ~4 ~3 ~34 minecraft:tinted_glass',
              'fill ~-2 ~0 ~34 ~2 ~2 ~34 minecraft:air',
              'fill ~-6 ~7 ~25 ~6 ~7 ~31 minecraft:polished_deepslate',
              'fill ~-6 ~8 ~25 ~6 ~9 ~25 minecraft:tinted_glass',
              'fill ~-6 ~8 ~31 ~6 ~9 ~31 minecraft:tinted_glass',
              'fill ~-6 ~8 ~25 ~-6 ~9 ~31 minecraft:tinted_glass',
              'fill ~6 ~8 ~25 ~6 ~9 ~31 minecraft:tinted_glass']
    for i,(x,z) in enumerate([(0,-20),(-17,10),(17,10)],1):
        lines += [f'setblock ~{x} ~0 ~{z} minecraft:lodestone',f'execute positioned ~{x} ~1 ~{z} run '+display('bell',(0,.5,0),tags=(f'nox.bell{i}',)),
                  f'summon minecraft:interaction ~{x} ~1 ~{z} {{Tags:["nox.owned","nox.bell","nox.bell{i}"],width:2f,height:2f,response:1b}}',
                  f'summon minecraft:text_display ~{x} ~3 ~{z} {{Tags:["nox.owned"],billboard:"center",text:{{text:"봉인종 {i}",color:"gold"}}}}']
    lines += ['execute positioned ~0 ~0 ~29 run '+display('device',(0,1,0)),
              'summon minecraft:interaction ~0 ~0 ~29 {Tags:["nox.owned","nox.start"],width:2f,height:2f,response:1b}',
              'summon minecraft:text_display ~0 ~2.5 ~29 {Tags:["nox.owned"],billboard:"center",line_width:240,text:{text:"일식 관측소\\n종을 우클릭하여 전투 시작\\n순서: 북쪽 1 → 동쪽 3 → 서쪽 2\\n입구 뒤에서 준비 후 중앙으로 진입",color:"gold"}}',
              call('arena/decorate'), 'tellraw @s {"text":"관측소 설치 완료. 입구는 남쪽(+Z), 중앙은 명령 실행 위치입니다.","color":"green"}']
    fn('arena/install',lines)
    decor=[]
    for r in [7,17,23]:
        for i in range(32):
            a=i*math.tau/32;x=math.cos(a)*r;z=math.sin(a)*r
            decor.append(f'execute positioned ~{x:.3f} ~.02 ~{z:.3f} run '+display('sigil',(0,0,0),(.5,.5,.5)))
    fn('arena/decorate',decor)
    fn('admin/unregister',[call('admin/abort'),'execute in minecraft:overworld run kill @e[tag=nox.owned]',
                           'scoreboard players set #installed nx.state 0','bossbar set eclipse_nox:health visible false',
                           'tellraw @s {"text":"녹스 등록과 엔티티 제거 완료. 설치한 블록은 남습니다.","color":"yellow"}'])
    fn('admin/start',['execute in minecraft:overworld if score #installed nx.state matches 1 if score #state nx.state matches 0 run '+at('fight/start')])
    fn('fight/start',['tag @a remove nox.member','tag @a remove nox.active',
                      'execute store result score #ymin nx.tmp run data get entity @s Pos[1] 100',
                      'scoreboard players operation #ymax nx.tmp = #ymin nx.tmp',
                      'scoreboard players remove #ymin nx.tmp 100','scoreboard players add #ymax nx.tmp 400',
                      'execute as @a[distance=..34,gamemode=survival] run '+call('fight/enroll'),
                      'execute as @a[distance=..34,gamemode=adventure] run '+call('fight/enroll'),
                      'execute if entity @a[tag=nox.member] run '+call('fight/begin')])
    fn('fight/enroll',['execute store result score @s nx.tmp run data get entity @s Pos[1] 100',
                      'execute if score @s nx.tmp >= #ymin nx.tmp if score @s nx.tmp <= #ymax nx.tmp run tag @s add nox.member'])
    begin=['scoreboard players set #state nx.state 1','scoreboard players set #phase nx.phase 1',
           'scoreboard players set #safe nx.safe 0','bossbar set eclipse_nox:health name {"text":"일식의 종지기, 녹스","color":"gold"}',
           'scoreboard players set #time nx.time 0','scoreboard players set #cast nx.cast 0','scoreboard players set #skill nx.skill 0',
           'scoreboard players set #idle nx.idle 0','scoreboard players set #grace nx.grace 300','scoreboard players set #next nx.next 80',
           'scoreboard players set #step nx.step 0','scoreboard players set #lock nx.lock 0','scoreboard players set #last nx.last 0','scoreboard players set #puzzle nx.puzzle 0',
           'scoreboard players set #max nx.max 400','execute as @a[tag=nox.member] run scoreboard players add #max nx.max 400',
           'execute if score #max nx.max matches 2001.. run scoreboard players set #max nx.max 2000',
           'scoreboard players add @a[tag=nox.member] nx.death 0','scoreboard players add @a[tag=nox.member] nx.leave 0',
           'execute as @a[tag=nox.member] run scoreboard players operation @s nx.olddeath = @s nx.death',
           'execute as @a[tag=nox.member] run scoreboard players operation @s nx.oldleave = @s nx.leave',
           'execute store result storage eclipse_nox:runtime hp int 1 run scoreboard players get #max nx.max',
           call('fight/summon')+' with storage eclipse_nox:runtime',
           'execute store result bossbar eclipse_nox:health max run scoreboard players get #max nx.max',
           'bossbar set eclipse_nox:health players @a[tag=nox.member]','bossbar set eclipse_nox:health visible true',
           'fill ~-4 ~0 ~23 ~4 ~3 ~24 minecraft:air',
           msg('녹스: 첫 종이 울렸다. 과거의 발자국을 기억하라.'),
           'playsound eclipse_nox:bell_low master @a[tag=nox.member] ~ ~ ~ 1 .6']
    fn('fight/begin',begin)
    fn('fight/summon',['$summon minecraft:ravager ~ ~ ~ {Tags:["nox.owned","nox.boss"],NoAI:1b,Silent:1b,PersistenceRequired:1b,Health:$(hp)f,attributes:[{id:"minecraft:max_health",base:$(hp)},{id:"minecraft:knockback_resistance",base:1.0},{id:"minecraft:scale",base:1.3}],DeathLootTable:"minecraft:empty",active_effects:[{id:"minecraft:invisibility",amplifier:0,duration:-1,show_particles:0b}]}',
                       display('body',(0,1.55,0),(1.8,1.8,1.8),('nox.bodypart',)),display('core',(0,1.7,-.55),(1.5,1.5,1.5),('nox.bodypart',)),
                       display('crown',(0,3.25,0),(1.5,1.5,1.5),('nox.bodypart',)),display('bell',(.95,1.3,0),(1.3,1.3,1.3),('nox.bodypart','nox.arm'))])
    tick=['execute in minecraft:overworld run '+call('tick_overworld')]
    fn('tick',tick)
    fn('tick_overworld',['execute if score #state nx.state matches 0 as @e[tag=nox.start] if data entity @s interaction run '+at('fight/start'),
                         'execute as @e[tag=nox.start] run data remove entity @s interaction',
                         'execute if score #state nx.state matches 1 as @e[tag=nox.anchor,limit=1] at @s run '+call('fight/tick'),
                         'execute unless score #state nx.state matches 1 as @e[tag=nox.bell,type=minecraft:interaction] run data remove entity @s interaction'])
    fight=['scoreboard players add #time nx.time 1','tag @a remove nox.active',
           'execute as @a[tag=nox.member,distance=..24,gamemode=survival] if score @s nx.death = @s nx.olddeath if score @s nx.leave = @s nx.oldleave run tag @s add nox.active',
           'execute as @a[tag=nox.member,distance=..24,gamemode=adventure] if score @s nx.death = @s nx.olddeath if score @s nx.leave = @s nx.oldleave run tag @s add nox.active',
           'execute as @a[tag=nox.member,distance=..26,tag=!nox.active] unless score #grace nx.grace matches 1.. run tp @s ~0 ~1 ~30',
           'execute as @a[tag=!nox.member,distance=..24,gamemode=!spectator] run tp @s ~0 ~1 ~30',
           'execute if score #grace nx.grace matches 1.. run scoreboard players remove #grace nx.grace 1',
           'execute if score #grace nx.grace matches 1 run fill ~-4 ~0 ~23 ~4 ~3 ~24 minecraft:tinted_glass',
           'execute unless entity @a[tag=nox.active] unless score #grace nx.grace matches 1.. run scoreboard players add #idle nx.idle 1',
           'execute if entity @a[tag=nox.active] run scoreboard players set #idle nx.idle 0',
           'execute if score #idle nx.idle matches 100.. run '+call('admin/abort'),
           'execute if score #state nx.state matches 1 unless entity @e[tag=nox.boss] run '+call('fight/victory'),
           'execute if score #state nx.state matches 1 run '+call('fight/alive')]
    fn('fight/tick',fight)
    alive=['execute store result score #hp nx.hp run data get entity @e[tag=nox.boss,limit=1] Health 100',
           'execute store result bossbar eclipse_nox:health value run data get entity @e[tag=nox.boss,limit=1] Health',
           'scoreboard players operation #ratio nx.tmp = #hp nx.hp','scoreboard players operation #ratio nx.tmp /= #max nx.max',
           'execute if score #phase nx.phase matches 1 if score #ratio nx.tmp matches ..65 run '+call('fight/phase2'),
           'execute if score #phase nx.phase matches 2 if score #ratio nx.tmp matches ..30 if score #puzzle nx.puzzle matches 0 run '+call('fight/phase3'),
           'execute if score #lock nx.lock matches 1.. run scoreboard players remove #lock nx.lock 1',
           'execute if score #safe nx.safe matches 1.. run scoreboard players remove #safe nx.safe 1',
           'execute if score #puzzle nx.puzzle matches 1 run '+call('puzzle/tick'),
           'execute if score #cast nx.cast matches 1.. run '+call('skills/casting'),
           'execute if score #cast nx.cast matches 0 if score #puzzle nx.puzzle matches 0 if entity @a[tag=nox.active] run scoreboard players remove #next nx.next 1',
           'execute if score #cast nx.cast matches 0 if score #puzzle nx.puzzle matches 0 if entity @a[tag=nox.active] if score #next nx.next matches ..0 run '+call('skills/begin'),
           'execute as @e[tag=nox.boss,limit=1] at @s if entity @a[tag=nox.active,distance=3..,limit=1] if score #cast nx.cast matches 0 if score #puzzle nx.puzzle matches 0 facing entity @a[tag=nox.active,sort=nearest,limit=1] feet run tp @s ^ ^ ^.055',
           'execute as @e[tag=nox.boss,limit=1] unless entity @s[distance=..21] run tp @s ~ ~ ~',
           'execute as @e[tag=nox.bodypart] at @e[tag=nox.boss,limit=1] run tp @s ~ ~ ~ ~ 0',call('visual/tick'),
           'execute if score #cast nx.cast matches 1.. run data modify entity @e[tag=nox.arm,limit=1] transformation.translation set value [0.95f,2.3f,0f]',
           'execute if score #cast nx.cast matches 0 run data modify entity @e[tag=nox.arm,limit=1] transformation.translation set value [0.95f,1.3f,0f]',
           'execute if score #safe nx.safe matches 1.. run data modify entity @e[tag=nox.core,limit=1] transformation.scale set value [2.5f,2.5f,2.5f]',
           'execute if score #safe nx.safe matches 0 run data modify entity @e[tag=nox.core,limit=1] transformation.scale set value [1.5f,1.5f,1.5f]',
           'execute if score #time nx.time matches 7200.. run '+call('admin/abort')]
    fn('fight/alive',alive)
    visual=['scoreboard players operation #frame nx.tmp = #time nx.time','scoreboard players set #five nx.tmp 5',
            'scoreboard players set #eight nx.tmp 8','scoreboard players operation #frame nx.tmp /= #five nx.tmp',
            'scoreboard players operation #frame nx.tmp %= #eight nx.tmp']
    for i in range(8):
        a=i*math.tau/8
        visual.append(f'execute if score #frame nx.tmp matches {i} run data modify entity @e[tag=nox.crown,tag=nox.bodypart,limit=1] transformation.left_rotation set value [0f,0f,{math.sin(a/2):.5f}f,{math.cos(a/2):.5f}f]')
    fn('visual/tick',visual)
    fn('fight/phase2',['scoreboard players set #phase nx.phase 2','scoreboard players set #puzzle nx.puzzle 1','scoreboard players set #cast nx.cast 0','kill @e[tag=nox.target]',
                      'bossbar set eclipse_nox:health name {"text":"녹스 · 봉인종의 공명","color":"gold"}',
                      'scoreboard players set #step nx.step 0','scoreboard players set #last nx.last 0','scoreboard players set #puzzletime nx.tmp 0',
                      'data merge entity @e[tag=nox.boss,limit=1] {Invulnerable:1b}',
                      msg('두 번째 종 — 봉인종을 우클릭: 북쪽 1 → 동쪽 3 → 서쪽 2. 같은 종을 연속 울리면 과부하!'),
                      'playsound eclipse_nox:bell_high master @a[tag=nox.member] ~ ~ ~ 1 .8'])
    fn('fight/phase3',['scoreboard players set #phase nx.phase 3','scoreboard players set #cast nx.cast 0','kill @e[tag=nox.target]',
                      'bossbar set eclipse_nox:health name {"text":"녹스 · 개기일식","color":"light_purple"}',
                      'scoreboard players set #next nx.next 60','scoreboard players set #skill nx.skill 3',
                      msg('개기일식 — 빛나는 회전 구역을 따라 이동하라. 종 주변은 잠시 안전하다.'),
                      'playsound eclipse_nox:bell_high master @a[tag=nox.member] ~ ~ ~ 1 .5'])
    fn('puzzle/tick',['scoreboard players add #puzzletime nx.tmp 1',
                      'execute as @e[tag=nox.bell,type=minecraft:interaction] if data entity @s interaction run '+call('puzzle/interact'),
                      'execute if score #puzzletime nx.tmp matches 100.. run '+call('puzzle/pulse'),
                      'execute if score #step nx.step matches 3 run '+call('puzzle/success')])
    fn('puzzle/interact',['tag @a remove nox.clicker','execute on target if entity @s[tag=nox.active] run tag @s add nox.clicker',
                          'execute if entity @a[tag=nox.clicker] if score #lock nx.lock matches 0 run '+call('puzzle/press'),
                          'data remove entity @s interaction','tag @a remove nox.clicker'])
    press=['scoreboard players set #bell nx.tmp 0']
    for i in range(1,4): press.append(f'execute if entity @s[tag=nox.bell{i}] run scoreboard players set #bell nx.tmp {i}')
    press+=['scoreboard players set #lock nx.lock 20','execute at @s run playsound eclipse_nox:bell_low master @a[tag=nox.member] ~ ~ ~ 1 1',
            'scoreboard players set #expected nx.tmp 1','execute if score #step nx.step matches 1 run scoreboard players set #expected nx.tmp 3',
            'execute if score #step nx.step matches 2 run scoreboard players set #expected nx.tmp 2',
            'execute if score #bell nx.tmp = #last nx.last at @s run '+call('puzzle/overload'),
            'execute if score #bell nx.tmp = #expected nx.tmp run scoreboard players add #step nx.step 1',
            'execute unless score #bell nx.tmp = #expected nx.tmp run scoreboard players set #step nx.step 0',
            'execute unless score #bell nx.tmp = #expected nx.tmp run '+msg('음이 어긋났다. 봉인종 순서를 처음부터 다시 맞춰라.'),
            'scoreboard players operation #last nx.last = #bell nx.tmp']
    fn('puzzle/press',press)
    fn('puzzle/overload',['summon minecraft:marker ~ ~ ~ {Tags:["nox.owned","nox.overload"]}',
                         'scoreboard players set @e[tag=nox.overload,sort=nearest,limit=1] nx.time 40',
                         msg('공명 과부하! 방금 울린 종에서 떨어지세요. 2초 후 폭발.')])
    fn('puzzle/pulse',['scoreboard players set #puzzletime nx.tmp 0','execute as @a[tag=nox.active] at @s run summon minecraft:marker ~ ~ ~ {Tags:["nox.owned","nox.echo"]}',
                      'scoreboard players set @e[tag=nox.echo] nx.time 60',msg('발자국이 기록됐다. 3초 후 잔향 폭발!')])
    fn('puzzle/success',['scoreboard players set #puzzle nx.puzzle 0','scoreboard players set #safe nx.safe 120','scoreboard players set #next nx.next 120',
                        'data merge entity @e[tag=nox.boss,limit=1] {Invulnerable:0b}',
                        'playsound eclipse_nox:expose master @a[tag=nox.member] ~ ~ ~ 1 1',msg('봉인 해제! 심장이 6초 동안 노출된다.')])
    # Timed hazards run in the encounter context, including puzzle and non-puzzle echoes.
    alive.insert(0,call('hazards/tick'))
    fn('fight/alive',alive)
    fn('hazards/tick',['scoreboard players remove @e[tag=nox.echo] nx.time 1','scoreboard players remove @e[tag=nox.overload] nx.time 1',
                       'execute as @e[tag=nox.echo] at @s run particle minecraft:reverse_portal ~ ~.1 ~ 1.3 .05 1.3 .01 12 force @a[tag=nox.member]',
                       'execute as @e[tag=nox.overload] at @s run particle minecraft:electric_spark ~ ~.5 ~ 2 .2 2 .02 15 force @a[tag=nox.member]',
                       'tag @a remove nox.hit','execute as @e[tag=nox.echo,scores={nx.time=..0}] at @s run '+call('hazards/echo'),
                       'tag @a remove nox.hit','execute as @e[tag=nox.overload,scores={nx.time=..0}] at @s run '+call('hazards/overload')])
    for name,r,damage in [('echo',2,6),('overload',4,6)]:
        fn('hazards/'+name,[f'execute as @a[tag=nox.active,tag=!nox.hit,distance=..{r}] run '+call(f'damage/{damage}'),
                            'particle minecraft:explosion ~ ~.5 ~ 1 .1 1 0 6 force @a[tag=nox.member]','kill @s'])
    for damage in [4,6,8]:
        fn(f'damage/{damage}',[f'damage @s {damage} minecraft:magic by @e[tag=nox.boss,limit=1]','tag @s add nox.hit'])
    fn('skills/begin',['scoreboard players add #skill nx.skill 1','execute if score #skill nx.skill matches 5.. run scoreboard players set #skill nx.skill 1',
                       'execute if score #phase nx.phase matches 1 if score #skill nx.skill matches 4 run scoreboard players set #skill nx.skill 1',
                       'execute if score #phase nx.phase matches 2 if score #skill nx.skill matches 4 run scoreboard players set #skill nx.skill 1',
                       'scoreboard players set #cast nx.cast 60','scoreboard players set #safe nx.safe 0',
                       'execute as @e[tag=nox.boss,limit=1] at @s facing entity @a[tag=nox.active,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0',
                       'execute at @e[tag=nox.boss,limit=1] facing entity @a[tag=nox.active,sort=nearest,limit=1] feet run summon minecraft:marker ~ ~ ~ {Tags:["nox.owned","nox.target"]}',
                       'execute as @e[tag=nox.target,limit=1] at @s facing entity @a[tag=nox.active,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0',
                       'execute if score #skill nx.skill matches 1 run '+msg('대종 내려치기 — 정면 부채꼴에서 벗어나세요!'),
                       'execute if score #skill nx.skill matches 2 run '+msg('고리 충격파 — 보스에게 붙거나 8블록 이상 떨어지세요!'),
                       'execute if score #skill nx.skill matches 3 run '+call('skills/echo'),
                       'execute if score #skill nx.skill matches 4 run '+call('skills/eclipse_begin'),
                       'playsound eclipse_nox:warning master @a[tag=nox.member] ~ ~ ~ 1 1'])
    fn('skills/echo',['execute as @a[tag=nox.active] at @s run summon minecraft:marker ~ ~ ~ {Tags:["nox.owned","nox.echo"]}',
                      'scoreboard players set @e[tag=nox.echo] nx.time 60',msg('잔향 낙인 — 지금 위치가 기록됐습니다. 3초 안에 이동하세요!')])
    fn('skills/casting',['scoreboard players remove #cast nx.cast 1',
                         'execute if score #skill nx.skill matches 1 at @e[tag=nox.target,limit=1] run '+call('skills/cleave_warn'),
                         'execute if score #skill nx.skill matches 2 at @e[tag=nox.target,limit=1] run '+call('skills/ring_warn'),
                         'execute if score #phase nx.phase matches 3 if score #skill nx.skill matches 2 if score #cast nx.cast matches 40 run tag @a remove nox.hit',
                         'execute if score #phase nx.phase matches 3 if score #skill nx.skill matches 2 if score #cast nx.cast matches 40 at @e[tag=nox.target,limit=1] run '+call('skills/ring_hit'),
                         'execute if score #phase nx.phase matches 3 if score #skill nx.skill matches 2 if score #cast nx.cast matches 20 run tag @a remove nox.hit',
                         'execute if score #phase nx.phase matches 3 if score #skill nx.skill matches 2 if score #cast nx.cast matches 20 at @e[tag=nox.target,limit=1] run '+call('skills/ring_hit'),
                         'execute if score #skill nx.skill matches 4 run '+call('skills/eclipse_tick'),
                         'execute if score #cast nx.cast matches 0 run '+call('skills/resolve')])
    cleave_warn=[];cleave_hit=[]
    for r in [2,4,6,8]:
        for a in [-40,-20,0,20,40]:
            x=math.sin(math.radians(a))*r;z=math.cos(math.radians(a))*r
            cleave_warn.append(f'execute rotated as @e[tag=nox.target,limit=1] positioned ^{x:.3f} ^.1 ^{z:.3f} run particle minecraft:flame ~ ~ ~ .25 .02 .25 0 1 force @a[tag=nox.member]')
            cleave_hit.append(f'execute rotated as @e[tag=nox.target,limit=1] positioned ^{x:.3f} ^ ^{z:.3f} as @a[tag=nox.active,tag=!nox.hit,distance=..1.7] run '+call('damage/8'))
    fn('skills/cleave_warn',cleave_warn);fn('skills/cleave_hit',cleave_hit)
    ringwarn=[]
    for i in range(48):
        a=i*math.tau/48
        for r in [4,7]: ringwarn.append(f'particle minecraft:soul_fire_flame ~{math.cos(a)*r:.3f} ~.1 ~{math.sin(a)*r:.3f} 0 0 0 0 1 force @a[tag=nox.member]')
    fn('skills/ring_warn',ringwarn)
    fn('skills/ring_hit',['execute as @a[tag=nox.active,tag=!nox.hit,distance=4..7] run '+call('damage/6')])
    fn('skills/resolve',['tag @a remove nox.hit','execute if score #skill nx.skill matches 1 at @e[tag=nox.target,limit=1] run '+call('skills/cleave_hit'),
                         'execute if score #skill nx.skill matches 2 at @e[tag=nox.target,limit=1] run '+call('skills/ring_hit'),
                         'kill @e[tag=nox.target]','scoreboard players set #next nx.next 80','scoreboard players set #safe nx.safe 30',
                         'execute if score #skill nx.skill matches 4 run scoreboard players set #next nx.next 120',
                         'execute if score #skill nx.skill matches 4 run scoreboard players set #safe nx.safe 120',
                         'playsound eclipse_nox:impact master @a[tag=nox.member] ~ ~ ~ .7 1'])
    # 8 positions, 40-tick warning, then six 40-tick rotations; cells have precise matching warning/hit areas.
    fn('skills/eclipse_begin',['scoreboard players set #cast nx.cast 280','scoreboard players set #angle nx.angle 0',
                               'scoreboard players set #rot nx.tmp 0',msg('일식 절정 — 청록빛 구역이 시계 방향으로 이동합니다. 다음 구역은 흰빛입니다.')])
    eclipse=['execute store result score #x nx.tmp run data get entity @s Pos[0] 100',
             'execute store result score #z nx.tmp run data get entity @s Pos[2] 100',
             'scoreboard players add #rot nx.tmp 1','execute if score #rot nx.tmp matches 40.. run scoreboard players set #rot nx.tmp 0',
             'execute if score #rot nx.tmp matches 0 run scoreboard players add #angle nx.angle 1',
             'execute if score #angle nx.angle matches 8.. run scoreboard players set #angle nx.angle 0']
    for i in range(8): eclipse.append(f'execute if score #angle nx.angle matches {i} run '+call(f'skills/eclipse/{i}'))
    fn('skills/eclipse_tick',eclipse)
    for i in range(8):
        lines=['tag @a remove nox.shelter',
               f'execute as @a[tag=nox.active] run '+call(f'skills/sector/{i}')]
        # Safe near the three bells during the first second of each shift.
        for x,z in [(0,-20),(-17,10),(17,10)]:
            lines.append(f'execute if score #rot nx.tmp matches ..20 positioned ~{x} ~ ~{z} run tag @a[tag=nox.active,distance=..3] add nox.shelter')
        for cell in range(8):
            for offset in [-20,0,20]:
                a=(cell*45+offset)*math.pi/180
                for r in [5,9,13,17,21]:
                    x=math.cos(a)*r;z=math.sin(a)*r
                    safe=cell==i;nextsafe=cell==(i+1)%8
                    p='end_rod' if nextsafe else 'electric_spark' if safe else 'soul_fire_flame'
                    lines.append(f'particle minecraft:{p} ~{x:.3f} ~.15 ~{z:.3f} .35 .02 .35 0 1 force @a[tag=nox.member]')
        lines+=['execute if score #cast nx.cast matches ..240 if score #rot nx.tmp matches 30 run tag @a remove nox.hit',
                'execute if score #cast nx.cast matches ..240 if score #rot nx.tmp matches 30 as @a[tag=nox.active,tag=!nox.shelter] run '+call('damage/4')]
        fn(f'skills/eclipse/{i}',lines)
        c=round(math.cos(i*math.pi/4)*1000);s=round(math.sin(i*math.pi/4)*1000)
        sector=['execute store result score @s nx.dx run data get entity @s Pos[0] 100',
                'execute store result score @s nx.dz run data get entity @s Pos[2] 100',
                'scoreboard players operation @s nx.dx -= #x nx.tmp','scoreboard players operation @s nx.dz -= #z nx.tmp',
                f'scoreboard players set #cos nx.tmp {c}',f'scoreboard players set #sin nx.tmp {s}',
                'scoreboard players set #thousand nx.tmp 1000','scoreboard players set #tan nx.tmp 414','scoreboard players set #negative nx.tmp -1',
                'scoreboard players operation @s nx.forward = @s nx.dx','scoreboard players operation @s nx.forward *= #cos nx.tmp',
                'scoreboard players operation @s nx.side = @s nx.dz','scoreboard players operation @s nx.side *= #sin nx.tmp',
                'scoreboard players operation @s nx.forward += @s nx.side','scoreboard players operation @s nx.forward /= #thousand nx.tmp',
                'scoreboard players operation @s nx.side = @s nx.dz','scoreboard players operation @s nx.side *= #cos nx.tmp',
                'scoreboard players operation @s nx.tmp = @s nx.dx','scoreboard players operation @s nx.tmp *= #sin nx.tmp',
                'scoreboard players operation @s nx.side -= @s nx.tmp','scoreboard players operation @s nx.side /= #thousand nx.tmp',
                'execute if score @s nx.side matches ..-1 run scoreboard players operation @s nx.side *= #negative nx.tmp',
                'scoreboard players operation @s nx.side *= #thousand nx.tmp','scoreboard players operation @s nx.forward *= #tan nx.tmp',
                'execute if score @s nx.forward matches 0.. if score @s nx.side <= @s nx.forward run tag @s add nox.shelter']
        fn(f'skills/sector/{i}',sector)
    fn('admin/abort',['execute in minecraft:overworld run '+call('fight/abort')])
    fn('fight/abort',['scoreboard players set #state nx.state 0',msg('전투가 중단되었습니다. 소환 장치에서 다시 시작할 수 있습니다.'),call('fight/cleanup')])
    fn('fight/victory',['scoreboard players set #state nx.state 0',msg('일식이 걷혔다. 녹스의 심장을 획득했습니다.'),
                        'execute as @a[tag=nox.member] if score @s nx.death = @s nx.olddeath if score @s nx.leave = @s nx.oldleave run '+call('reward'),
                        'playsound eclipse_nox:victory master @a[tag=nox.member] ~ ~ ~ 1 1',call('fight/cleanup')])
    fn('reward',['give @s minecraft:amethyst_shard[minecraft:item_model="eclipse_nox:relic",minecraft:item_name={"text":"일식의 심장","color":"light_purple"},minecraft:lore=[{"text":"일식의 종지기 녹스 처치 증표","color":"gray"}],minecraft:custom_data={nox_relic:1b}] 1',
                 'give @s minecraft:diamond 4','experience add @s 500 points'])
    fn('fight/cleanup',['kill @e[tag=nox.bodypart]','kill @e[tag=nox.boss]','kill @e[tag=nox.target]','kill @e[tag=nox.echo]','kill @e[tag=nox.overload]',
                        'execute as @e[tag=nox.bell,type=minecraft:interaction] run data remove entity @s interaction',
                        'bossbar set eclipse_nox:health visible false','bossbar set eclipse_nox:health players',
                        'scoreboard players set #cast nx.cast 0','scoreboard players set #puzzle nx.puzzle 0',
                        'tag @a remove nox.member','tag @a remove nox.active',
                        'execute at @e[tag=nox.anchor,limit=1] run fill ~-4 ~0 ~23 ~4 ~3 ~24 minecraft:air'])
    from worldgen import upgrade_worldgen
    from motion import upgrade_motion
    from combat import upgrade_combat
    from timing import apply_fast_timing
    upgrade_worldgen()
    upgrade_motion()
    upgrade_combat()
    apply_fast_timing()
    from expansion import upgrade_expansion
    upgrade_expansion()
    from minions import upgrade_minions
    upgrade_minions()
    validate_and_package()

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def validate_and_package():
    OUT.mkdir(parents=True,exist_ok=True)
    functions=list((DP/f'data/{NS}/function').rglob('*.mcfunction'))
    for p in functions:
        content=p.read_text(encoding='utf-8')
        for ref in re.findall(r'function eclipse_nox:([a-z0-9_/]+)(?=\s|$)',content,re.M):
            assert (DP/f'data/{NS}/function/{ref}.mcfunction').is_file(),(p,ref)
        assert 'dungeons_arise:' not in content
    for p in list(DP.rglob('*.json'))+list(RP.rglob('*.json')): json.loads(p.read_text(encoding='utf-8'))
    for name in ['body','core','crown','bell','sigil','relic','device']:
        model=json.loads((RP/f'assets/{NS}/models/{name}.json').read_text())
        assert all(-16<=v<=32 for e in model['elements'] for v in e['from']+e['to'])
    def zipdir(folder,dest):
        with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
            for p in sorted(folder.rglob('*')):
                if p.is_file(): z.write(p,p.relative_to(folder).as_posix())
    zipdir(DP,OUT/'Nox-Standalone-Datapack-26.3.zip')
    zipdir(RP,OUT/'Nox-Additional-Resources-26.3.zip')
    source=ROOT/'ida26/output/IDA-Integrated-Boss-Resources-26.3-TextureFix.zip'
    if not source.is_file(): source=ROOT/'ida26/output/IDA-Integrated-Boss-Resources-26.3.zip'
    original_hash=sha(source)
    merged=OUT/'Integrated-Resources-with-Nox-26.3.zip'
    with zipfile.ZipFile(source) as src,zipfile.ZipFile(merged,'w',zipfile.ZIP_DEFLATED) as dest:
        atlas_path='assets/minecraft/atlases/items.json'
        atlas=json.loads(src.read(atlas_path)) if atlas_path in src.namelist() else {'sources':[]}
        atlas['sources']+=json.loads((RP/atlas_path).read_text())['sources']
        for info in src.infolist():
            if info.filename not in ['pack.mcmeta',atlas_path] and not info.is_dir(): dest.writestr(info,src.read(info.filename))
        for p in sorted(RP.rglob('*')):
            if p.is_file() and p.relative_to(RP).as_posix() not in ['pack.mcmeta',atlas_path]:
                assert p.relative_to(RP).as_posix() not in src.namelist()
                dest.write(p,p.relative_to(RP).as_posix())
        dest.writestr(atlas_path,json.dumps(atlas,ensure_ascii=False,indent=2))
        dest.writestr('pack.mcmeta',json.dumps({'pack':{'min_format':[97,1],'max_format':[97,1],'description':'Integrated IDA Resources + Nox — Java 26.3'}},ensure_ascii=False))
    assert sha(source)==original_hash
    with zipfile.ZipFile(source) as src,zipfile.ZipFile(merged) as dest:
        for n in src.namelist():
            if not n.endswith('/') and n not in ['pack.mcmeta','assets/minecraft/atlases/items.json']: assert src.read(n)==dest.read(n),n
    js(OUT/'static-validation.json',{'revision':2,'functions':len(functions),'independent_namespace':True,'resource_models':len(list((RP/f'assets/{NS}/models').glob('*.json'))),'articulated_joints':10,'animation_modes':8,'animation_frames_per_mode':16,'native_underground_worldgen':True,'source_resource_pack':str(source),'source_sha256':original_hash,'source_unchanged':True,'existing_assets_preserved':True,'merged_atlas':True,'limitations':['Engine validation is a separate step; no client render or player combat test.']})
    js(OUT/'SHA256.json',{p.name:sha(p) for p in OUT.glob('*.zip')})
    print('Built',len(functions),'functions, 10 joints and native underground worldgen; original resources preserved.')

if __name__=='__main__': build()
