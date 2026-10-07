"""Faster encounter, phase-three execution and custom model minions."""
import json, struct, zlib, math
from build import DP, RP, NS, fn, call, msg, js, display, OUT
from timing import patch

def read(name): return (DP/f'data/{NS}/function/{name}.mcfunction').read_text(encoding='utf-8').splitlines()
def add(name,lines): fn(name,read(name)+lines)

def upgrade_expansion():
    for name in ['skills/begin','skills/echo','puzzle/pulse','puzzle/overload']:
        p=DP/f'data/{NS}/function/{name}.mcfunction'
        text=p.read_text(encoding='utf-8').replace('#cast nx.cast 30','#cast nx.cast 20').replace('#cast nx.cast 24','#cast nx.cast 16').replace('nx.time 30','nx.time 20').replace('1.5초','1초')
        fn(name,text.rstrip().splitlines())
    patch('skills/combo',[('#cast nx.cast 20','#cast nx.cast 12'),('#total nx.total 20','#total nx.total 12')])
    patch('skills/recover',[('#safe nx.safe 25','#safe nx.safe 12'),('#safe nx.safe 35','#safe nx.safe 20'),('#next nx.next 5','#next nx.next 2')])
    patch('skills/dash/end',[('#safe nx.safe 30','#safe nx.safe 16'),('#safe nx.safe 35','#safe nx.safe 20'),('#next nx.next 5','#next nx.next 2')])
    patch('puzzle/success',[('#safe nx.safe 35','#safe nx.safe 20'),('#next nx.next 5','#next nx.next 2'),('1.75초','1초')])
    patch('puzzle/tick',[('matches 40..','matches 24..')])
    patch('fight/begin',[('#next nx.next 30','#next nx.next 20')])
    patch('visual/frame/recover',[('#frame nx.tmp 25','#frame nx.tmp 12'),('#thirty nx.tmp 25','#thirty nx.tmp 12')])
    add('load',['scoreboard objectives add nx.add dummy','scoreboard objectives add nx.doom dummy'])
    add('fight/begin',['scoreboard players set #adds nx.add 0','scoreboard players set #doom nx.doom 0','scoreboard players set #judgement nx.doom 0',call('minions/spawn')])
    add('fight/phase2',[call('minions/spawn')])
    add('fight/phase3',['scoreboard players set #doom nx.doom 80',call('minions/spawn'),msg('최후의 심판 — 붉은 예고가 나타나면 중앙 금빛 원(반경 4블록)으로! 밖은 즉사합니다.')])
    alive=read('fight/alive');alive.insert(0,call('expansion/tick'));fn('fight/alive',alive)
    add('fight/cleanup',['kill @e[tag=nox.minion]','kill @e[tag=nox.minion_visual]','scoreboard players set #judgement nx.doom 0','tag @a remove nox.doom_safe'])
    add('tick_overworld',['execute if score #state nx.state matches 0 run kill @e[tag=nox.minion]','execute if score #state nx.state matches 0 run kill @e[tag=nox.minion_visual]'])
    fn('expansion/tick',[call('minions/tick'),
        'execute if score #phase nx.phase matches 3 run scoreboard players remove #doom nx.doom 1',
        'execute if score #judgement nx.doom matches 1.. run '+call('judgement/tick'),
        'execute if score #phase nx.phase matches 3 if score #doom nx.doom matches ..0 if score #judgement nx.doom matches 0 if score #cast nx.cast matches 0 if score #dash nx.dash matches 0 if score #puzzle nx.puzzle matches 0 run '+call('judgement/begin')])
    # The judgement owns cast time so no normal attack can start during its warning.
    fn('judgement/begin',['scoreboard players set #judgement nx.doom 40','scoreboard players set #doom nx.doom 160','scoreboard players set #cast nx.cast 41','scoreboard players set #skill nx.skill 6','scoreboard players set #total nx.total 41',msg('최후의 심판! 2초 안에 중앙 금빛 원으로 들어오세요!'),'playsound minecraft:entity.wither.spawn master @a[tag=nox.member] ~ ~ ~ .6 1.5'])
    warn=[]
    for i in range(40):
        a=i*math.tau/40
        warn.append(f'particle minecraft:end_rod ~{math.cos(a)*4:.3f} ~.2 ~{math.sin(a)*4:.3f} 0 .3 0 0 1 force @a[tag=nox.member]')
        warn.append(f'particle minecraft:dust{{color:[1.0,0.05,0.1],scale:2.0}} ~{math.cos(a)*12:.3f} ~.2 ~{math.sin(a)*12:.3f} 1 .1 1 0 1 force @a[tag=nox.member]')
    fn('judgement/tick',['scoreboard players remove #judgement nx.doom 1']+warn+['execute if score #judgement nx.doom matches 0 run '+call('judgement/resolve')])
    fn('judgement/resolve',['tag @a remove nox.doom_safe','tag @a[tag=nox.active,distance=..4] add nox.doom_safe','execute as @a[tag=nox.active,tag=!nox.doom_safe] run damage @s 1000000 minecraft:generic_kill','scoreboard players set #cast nx.cast 0','scoreboard players set #safe nx.safe 16','scoreboard players set #next nx.next 2','scoreboard players set #expose nx.expose 1','playsound minecraft:entity.warden.sonic_boom master @a[tag=nox.member] ~ ~ ~ 1 .6',msg('심판 종료 — 녹스의 심장이 잠시 노출됩니다!')])
    # Quarter ranged damage; melee, dash and phase-three execution keep their roles.
    patch('damage/4',[('damage @s 4 minecraft:magic','damage @s 1 minecraft:magic')])
    patch('damage/6',[('damage @s 6 minecraft:magic','damage @s 1.5 minecraft:magic')])
    add('skills/dash/begin',['scoreboard players set #counter nx.move 0','scoreboard players set #crash nx.move 0'])
    fn('skills/dash/end',['kill @e[tag=nox.target]','scoreboard players set #safe nx.safe 16','scoreboard players set #next nx.next 2','scoreboard players set #expose nx.expose 0','scoreboard players set #counter nx.move 0',
        'execute if score #crash nx.move matches 1 run '+call('skills/dash/counter'), 'scoreboard players set #crash nx.move 0'])
    fn('skills/dash/counter',['scoreboard players set #safe nx.safe 40','scoreboard players set #next nx.next 0','scoreboard players set #expose nx.expose 1','scoreboard players set #counter nx.move 1',
        'execute store result score #oldhp nx.hp run data get entity @e[tag=nox.boss,limit=1] Health 100',
        'playsound eclipse_nox:expose master @a[tag=nox.member] ~ ~ ~ 1 1.4',msg('벽 충돌! 2초 동안 카운터 가능 — 녹스에게 주는 피해 2배!')])
    patch('fight/bonus',[('scoreboard players set #two nx.tmp 2','scoreboard players set #two nx.tmp 2\nexecute if score #counter nx.move matches 1 run scoreboard players set #two nx.tmp 1')])
    add('fight/exposure',['execute if score #safe nx.safe matches 0 run scoreboard players set #counter nx.move 0'])
    for name in ['fight/begin','fight/cleanup']:
        add(name,['scoreboard players set #counter nx.move 0'])
    patch('expansion/tick',[('if score #puzzle nx.puzzle matches 0 run '+call('judgement/begin'),'if score #puzzle nx.puzzle matches 0 if score #safe nx.safe matches 0 run '+call('judgement/begin'))])
    # Native husk AI drives melee and is hidden behind dedicated mounted item models.
    atlas=json.loads((RP/'assets/minecraft/atlases/items.json').read_text())
    for name,palette in [('acolyte',['211a35','684b91','b595e5','69f0ff']),('warden',['211c22','72523f','d7a54b','ff514d'])]:
        pixels=bytearray()
        for y in range(32):
            pixels.append(0)
            for x in range(64):
                c=bytes.fromhex(palette[x//16]); d=22 if (x+2*y)%9==0 else -18 if x%16 in (0,15) else 0
                pixels.extend([max(0,min(255,v+d)) for v in c]+[255])
        def chunk(t,b):return struct.pack('>I',len(b))+t+b+struct.pack('>I',zlib.crc32(t+b)&0xffffffff)
        (RP/f'assets/{NS}/textures/entity/{name}.png').write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',64,32,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(pixels))+chunk(b'IEND',b''))
        def box(center,size,mat):return {'from':[8+c-s/2 for c,s in zip(center,size)],'to':[8+c+s/2 for c,s in zip(center,size)],'faces':{f:{'texture':'#atlas','uv':[mat*4,0,mat*4+4,16]} for f in ['up','down','north','south','east','west']}}
        elements=[box((0,0,0),(10,13,7),0),box((0,10,0),(8,7,8),1),box((0,10,-4),(6,2,1),3),box((-7,0,0),(4,12,5),2),box((7,0,0),(4,12,5),2),box((-3,-10,0),(4,7,5),0),box((3,-10,0),(4,7,5),0)]
        if name=='warden':elements += [box((0,15,0),(12,2,10),2),box((8,-3,-3),(5,14,2),2)]
        js(RP/f'assets/{NS}/models/{name}.json',{'textures':{'atlas':f'{NS}:entity/{name}'},'elements':elements})
        js(RP/f'assets/{NS}/items/{name}.json',{'model':{'type':'minecraft:model','model':f'{NS}:{name}'}})
        atlas['sources'].append({'type':'minecraft:single','resource':f'{NS}:entity/{name}','sprite':f'{NS}:entity/{name}'})
        passenger=json.loads(display(name,(0,-.45,0),(.9,.9,.9),('nox.minion_visual',)).split(' ~ ~ ~ ',1)[1]);passenger['id']='minecraft:item_display';passenger['Tags'].append('nox.minion.'+name)
        mob={'Tags':['nox.owned','nox.minion','nox.add.'+name],'PersistenceRequired':True,'Silent':True,'Health':24 if name=='acolyte' else 36,'attributes':[{'id':'minecraft:max_health','base':24 if name=='acolyte' else 36},{'id':'minecraft:movement_speed','base':.29 if name=='acolyte' else .23},{'id':'minecraft:attack_damage','base':3 if name=='acolyte' else 5}],'active_effects':[{'id':'minecraft:invisibility','amplifier':0,'duration':2147483647,'show_particles':False}],'Passengers':[passenger]}
        fn('minions/spawn_'+name,['summon minecraft:husk ~ ~ ~ '+json.dumps(mob,separators=(',',':'))])
    js(RP/'assets/minecraft/atlases/items.json',atlas)
    fn('minions/spawn',['execute unless entity @e[tag=nox.minion,limit=4] positioned ~-10 ~ ~-8 run '+call('minions/spawn_acolyte'),'execute positioned ~10 ~ ~8 unless entity @e[tag=nox.minion,distance=..40,limit=6] run '+call('minions/spawn_warden')])
    # Count explicitly: selector limit alone does not enforce a population ceiling.
    fn('minions/spawn',['execute store result score #count nx.add if entity @e[tag=nox.minion]','execute if score #count nx.add matches ..4 positioned ~-10 ~ ~-8 run '+call('minions/spawn_acolyte'),'execute if score #count nx.add matches ..4 positioned ~10 ~ ~8 run '+call('minions/spawn_warden')])
    fn('minions/tick',['scoreboard players add #adds nx.add 1','execute if score #adds nx.add matches 100.. run '+call('minions/reinforce'),'tag @e[tag=nox.minion_visual] remove nox.riding','execute as @e[tag=nox.minion] on passengers run tag @s add nox.riding','kill @e[tag=nox.minion_visual,tag=!nox.riding]','execute as @e[tag=nox.minion_visual] at @s run particle minecraft:soul ~ ~.5 ~ .1 .2 .1 .01 1 normal @a[tag=nox.member]','execute as @e[tag=nox.minion] at @s unless entity @e[tag=nox.anchor,tag=nox.current,distance=..23] run tp @s ~ ~ ~ facing entity @e[tag=nox.anchor,tag=nox.current,limit=1] feet','execute as @e[tag=nox.minion] at @s unless entity @e[tag=nox.anchor,tag=nox.current,distance=..24] at @e[tag=nox.anchor,tag=nox.current,limit=1] run tp @s ~ ~ ~'])
    fn('minions/reinforce',['scoreboard players set #adds nx.add 0',call('minions/spawn')])
    js(OUT/'timing-profile.json',{'ticks_per_second':20,'telegraph_ticks':{'cleave':20,'second_cleave':12,'dash':16,'echo':20,'ring':20,'judgement':40},'recovery_plus_idle_ticks':{'normal':14,'dash':18,'stagger':22},'minion_reinforcement_ticks':100,'minion_cap':6,'judgement_retry_ticks':160,'judgement_safe_radius':4,'ranged_damage_multiplier':0.25,'wall_counter_ticks':40,'wall_counter_damage_multiplier':2})
