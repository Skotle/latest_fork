"""Native underground worldgen, symmetrical shell, and per-site activation."""
import gzip, math, re, struct
from build import DP, NS, ROOT, fn, js, call, at

# Independent minimal NBT writer; deployment and build do not depend on IDA.
class Tag:
    def __init__(self, kind, value):self.kind,self.value=kind,value
def nbt(root):
    out=bytearray()
    def string(s):
        b=s.encode('utf-8');out.extend(struct.pack('>H',len(b)));out.extend(b)
    def payload(k,v):
        if k in (1,3,6):out.extend(struct.pack({1:'>b',3:'>i',6:'>d'}[k],v))
        elif k==8:string(v)
        elif k==9:
            subtype,values=v;out.extend(struct.pack('>Bi',subtype,len(values)))
            for value in values:payload(subtype,value)
        elif k==10:
            for name,t in v.items():out.append(t.kind);string(name);payload(t.kind,t.value)
            out.append(0)
        else:raise ValueError(k)
    out.append(10);string('');payload(10,root)
    return bytes(out)

def template():
    blocks={}
    def put(x,y,z,b):blocks[(x+34,y+2,z+34)]=b
    # Only the chamber and four access galleries replace terrain. Outside is omitted.
    for x in range(-25,26):
        for z in range(-25,26):
            r=math.hypot(x,z)
            if r>25.5:continue
            for y in range(-2,18):
                if y in (-2,17) or r>24.5:b='minecraft:deepslate_bricks'
                elif y==-1:
                    b='minecraft:chiseled_deepslate' if any(abs(r-v)<.45 for v in [7,17,23]) else 'minecraft:deepslate_tiles' if (x+z)%2==0 else 'minecraft:polished_blackstone'
                elif r>23.3 and y<4:b='minecraft:tinted_glass'
                else:b='minecraft:air'
                if y==17 and (x%8==0 or z%8==0):b='minecraft:chiseled_deepslate'
                if y==16 and abs(r-21)<.5 and (x%5==0 or z%5==0):b='minecraft:sea_lantern'
                put(x,y,z,b)
    # Four-way symmetry makes random jigsaw rotation irrelevant to bell directions.
    for turn in range(4):
        def rot(x,z):
            for _ in range(turn):x,z=-z,x
            return x,z
        for x in range(-5,6):
            for z in range(23,35):
                for y in range(-2,13):
                    if y in (-2,-1):b='minecraft:polished_deepslate'
                    elif y==4 or abs(x)==5:b='minecraft:polished_blackstone_bricks'
                    elif y>=5:b='minecraft:deepslate_bricks' if y==12 else 'minecraft:air'
                    else:b='minecraft:air'
                    if z<=24 and abs(x)<=4 and y in range(0,5):b='minecraft:air'
                    if z==34 and abs(x)>2 and y in range(0,4):b='minecraft:tinted_glass'
                    if y==7 and 25<=z<=31:b='minecraft:polished_deepslate'
                    if y==8 and (abs(x)==5 or z in (25,31)):b='minecraft:tinted_glass'
                    if y==3 and z in (27,32) and abs(x)==4:b='minecraft:sea_lantern'
                    X,Z=rot(x,z);put(X,y,Z,b)
        # Short mining approach gallery: open end into surrounding stone/caves.
        # Entrance is visibly marked; existing terrain outside the template stays intact.
    palette=sorted(set(blocks.values()));ids={b:i for i,b in enumerate(palette)}
    entries=[{'pos':Tag(9,(3,list(p))), 'state':Tag(3,ids[b])} for p,b in sorted(blocks.items())]
    seed={'id':Tag(8,'minecraft:marker'),'Tags':Tag(9,(8,['nox.owned','nox.seed','nox.site'])),
          'data':Tag(10,{'version':Tag(3,2)})}
    entity={'pos':Tag(9,(6,[34.,2.,34.])), 'blockPos':Tag(9,(3,[34,2,34])), 'nbt':Tag(10,seed)}
    root={'DataVersion':Tag(3,5023),'size':Tag(9,(3,[69,20,69])),
          'palette':Tag(9,(10,[{'id':Tag(8,b)} for b in palette])),
          'blocks':Tag(9,(10,entries)), 'entities':Tag(9,(10,[entity]))}
    p=DP/f'data/{NS}/structure/observatory.nbt';p.parent.mkdir(parents=True,exist_ok=True)
    p.write_bytes(gzip.compress(nbt(root),mtime=0))
    js(DP/f'data/{NS}/worldgen/structure/observatory.json',{
        'type':'minecraft:jigsaw','biomes':'#minecraft:is_overworld','step':'underground_structures',
        'spawn_overrides':{'monster':{'bounding_box':'piece','spawns':[]}},'terrain_adaptation':'none','start_pool':f'{NS}:observatory',
        'size':1,'start_height':{'type':'minecraft:uniform','min_inclusive':{'absolute':-46},'max_inclusive':{'absolute':-22}},
        'max_distance_from_center':80,'use_expansion_hack':False,'liquid_settings':'ignore_waterlogging'})
    js(DP/f'data/{NS}/worldgen/template_pool/observatory.json',{
        'name':f'{NS}:observatory','fallback':'minecraft:empty','elements':[{'weight':1,'element':{
        'element_type':'minecraft:single_pool_element','location':f'{NS}:observatory','processors':'minecraft:empty','projection':'rigid'}}]})
    js(DP/f'data/{NS}/worldgen/structure_set/observatories.json',{
        'structures':[{'structure':f'{NS}:observatory','weight':1}],
        'placement':{'type':'minecraft:random_spread','spacing':48,'separation':24,'salt':73102631}})
    return len(entries)

def upgrade_worldgen():
    count=template()
    path=DP/f'data/{NS}/function/arena/install.mcfunction'
    old=path.read_text(encoding='utf-8').splitlines()
    # Reuse the validated bell/device authoring, not the destructive floor builder.
    start=next(i for i,l in enumerate(old) if l=='setblock ~0 ~0 ~-20 minecraft:lodestone')
    setup=old[start:-1]
    fn('site/init',['tag @s remove nox.seed','tag @s add nox.anchor','tag @s add nox.site',
                    'scoreboard players set #installed nx.state 1',
                    'scoreboard players add #site nx.tmp 1','scoreboard players operation @s nx.tmp = #site nx.tmp',
                    *setup])
    fn('arena/install',['place template eclipse_nox:observatory ~-34 ~-2 ~-34',
                       'execute as @e[tag=nox.seed,distance=..2] at @s run '+call('site/init'),
                       'tellraw @s {"text":"지하 관측소 설치 완료. 자연 생성은 새 청크에서 작동합니다.","color":"green"}'])
    fn('admin/install',['execute unless dimension minecraft:overworld run tellraw @s {"text":"관측소는 오버월드에서만 설치할 수 있습니다.","color":"yellow"}',
                        'execute if dimension minecraft:overworld if score #state nx.state matches 0 positioned ~ ~ ~ align xyz run '+call('arena/install')])
    fn('site/request',['execute if score #state nx.state matches 1 run tellraw @a[distance=..38] {"text":"다른 관측소에서 전투가 진행 중입니다.","color":"gray"}',
                       'execute if score #state nx.state matches 0 run '+call('site/select')])
    fn('site/select',['tag @e[tag=nox.anchor] remove nox.current',
                      'tag @e[tag=nox.anchor,distance=..40,sort=nearest,limit=1] add nox.current',
                      'scoreboard players operation #active_site nx.tmp = @e[tag=nox.current,limit=1] nx.tmp',
                      at('fight/start'),
                      'execute unless score #state nx.state matches 1 run tag @e[tag=nox.current] remove nox.current'])
    fn('admin/start',['execute in minecraft:overworld run '+call('site/request')])
    fn('tick_overworld',[
        'execute as @e[tag=nox.seed] at @s if entity @a[distance=..88] run '+call('site/init'),
        'execute as @e[tag=nox.anchor] unless score @s nx.tmp matches 1.. run '+call('site/identify'),
        'execute if score #state nx.state matches 1 as @e[tag=nox.anchor,tag=nox.current] unless score @s nx.tmp = #active_site nx.tmp at @s run '+call('site/retire'),
        'execute if score #state nx.state matches 1 unless entity @e[tag=nox.anchor,tag=nox.current] run '+call('fight/abort'),
        'execute if score #state nx.state matches 0 as @e[tag=nox.anchor,tag=nox.current] at @s run '+call('arena/open'),
        'execute if score #state nx.state matches 0 run tag @e[tag=nox.current] remove nox.current',
        'execute if score #state nx.state matches 0 run kill @e[tag=nox.target]',
        'execute if score #state nx.state matches 0 run kill @e[tag=nox.echo]',
        'execute if score #state nx.state matches 0 run kill @e[tag=nox.overload]',
        'execute if score #state nx.state matches 0 as @e[tag=nox.start] at @s if data entity @s interaction run '+call('site/request'),
        'execute as @e[tag=nox.start] run data remove entity @s interaction',
        'execute if score #state nx.state matches 1 as @e[tag=nox.anchor,tag=nox.current,limit=1] at @s run '+call('fight/tick'),
        'execute unless score #state nx.state matches 1 as @e[tag=nox.bell,type=minecraft:interaction] run data remove entity @s interaction',
        'execute if score #state nx.state matches 0 run kill @e[tag=nox.bodypart]',
        'execute if score #state nx.state matches 0 run kill @e[tag=nox.boss]'])
    fn('site/identify',['scoreboard players add #site nx.tmp 1','scoreboard players operation @s nx.tmp = #site nx.tmp'])
    fn('site/retire',[call('arena/open'),'kill @e[tag=nox.boss,distance=..26]','kill @e[tag=nox.bodypart,distance=..26]',
                      'kill @e[tag=nox.echo,distance=..34]','kill @e[tag=nox.target,distance=..26]','kill @e[tag=nox.overload,distance=..34]',
                      'tag @s remove nox.current'])
    fn('admin/unregister',['execute if score #state nx.state matches 0 in minecraft:overworld as @e[tag=nox.anchor,distance=..40,sort=nearest,limit=1] at @s run '+call('site/remove'),
                           'execute if score #state nx.state matches 1 run tellraw @s {"text":"먼저 전투를 중단하세요: /function eclipse_nox:admin/abort","color":"yellow"}'])
    fn('site/remove',['kill @e[tag=nox.owned,distance=..40]'])
    fn('arena/open',['fill ~-4 ~0 ~23 ~4 ~3 ~24 minecraft:air','fill ~-4 ~0 ~-24 ~4 ~3 ~-23 minecraft:air',
                     'fill ~23 ~0 ~-4 ~24 ~3 ~4 minecraft:air','fill ~-24 ~0 ~-4 ~-23 ~3 ~4 minecraft:air'])
    fn('arena/close',[l.replace('minecraft:air','minecraft:tinted_glass') for l in (DP/f'data/{NS}/function/arena/open.mcfunction').read_text().splitlines()])
    def modify(name,change):
        p=DP/f'data/{NS}/function/{name}.mcfunction';fn(name,change(p.read_text(encoding='utf-8').splitlines()))
    modify('fight/begin',lambda lines:[call('arena/open') if l.startswith('fill ~-4 ~0 ~23') else l for l in lines])
    modify('fight/tick',lambda lines:[l.replace('run fill ~-4 ~0 ~23 ~4 ~3 ~24 minecraft:tinted_glass','run '+call('arena/close')) for l in lines])
    modify('fight/cleanup',lambda lines:[l.replace('@e[tag=nox.anchor,limit=1]','@e[tag=nox.anchor,tag=nox.current,limit=1]').replace('run fill ~-4 ~0 ~23 ~4 ~3 ~24 minecraft:air','run '+call('arena/open')) for l in lines]+['tag @e[tag=nox.current] remove nox.current'])
    modify('load',lambda lines:[l for l in lines if not l.startswith('tellraw @a')]+[
        'tellraw @a {"text":"[녹스 v2] 관측소가 새 오버월드 청크의 지하에 생성됩니다. /locate structure eclipse_nox:observatory","color":"gray"}'])
    js(DP/f'data/{NS}/worldgen-notes.json',{'template_blocks':count,'arena_floor_y':[-45,-21],'roof_y':[-28,-4],'spacing_chunks':48,'separation_chunks':24,'worldgen_entities':1})
