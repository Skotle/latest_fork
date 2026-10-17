"""Build vanilla-only eight difficulty presets for Java 26.3."""
import json, zipfile, hashlib
from pathlib import Path

BASE=Path(__file__).resolve().parent
PACK=BASE/'datapack'
NS='infernal'
function_root=PACK/'data'/NS/'function'
for old in function_root.rglob('*.mcfunction'):
    old.resolve().relative_to(function_root.resolve())
    old.unlink()
def js(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def fn(name,lines):
    p=PACK/'data'/NS/'function'/(name+'.mcfunction');p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
def tag(name,values):js(PACK/'data'/NS/'tags/entity_type'/(name+'.json'),{'values':['minecraft:'+v for v in values]})
melee='zombie husk drowned zombie_villager zombified_piglin piglin piglin_brute wither_skeleton spider cave_spider silverfish endermite enderman hoglin zoglin vindicator vex ravager'.split()
ranged='skeleton stray bogged pillager evoker witch creeper blaze ghast phantom guardian shulker breeze'.split()
tag('ordinary',melee+ranged+['slime','magma_cube'])
tag('melee',melee)
tag('armor','zombie husk drowned zombie_villager skeleton stray bogged'.split())
tag('zombie','zombie husk drowned zombie_villager'.split())
tag('archer','skeleton stray bogged'.split())
tag('boss',['ender_dragon','wither','elder_guardian'])
js(PACK/'data/infernal/tags/entity_type/eligible.json',{'values':['#infernal:ordinary','#infernal:boss']})
js(PACK/'pack.mcmeta',{'pack':{'min_format':[121,0],'max_format':[121,0],'description':'Infernal Difficulties — 8 vanilla presets / Java 26.3'}})
for name in ['load','tick']:js(PACK/f'data/minecraft/tags/function/{name}.json',{'values':[f'infernal:{name}']})
fn('load',['scoreboard objectives add inf.sys dummy','scoreboard objectives add inf.rev dummy','scoreboard objectives add inf.id dummy','execute unless score #level inf.sys matches 0..7 run function infernal:init','tellraw @a {text:"[Infernal] /function infernal:menu",color:"gold"}'])
fn('init',['execute store result score #level inf.sys run difficulty','scoreboard players set #epoch inf.sys 1','scoreboard players set #serial inf.sys 0','scoreboard players set #clock inf.sys 0'])
names=['peaceful','easy','normal','hard','harder','insane','demon','nightmare']
for i,name in enumerate(names):
    fn('set/'+name,[f'execute if score #level inf.sys matches {i} run return 0',f'scoreboard players set #level inf.sys {i}','scoreboard players add #epoch inf.sys 1',f'difficulty {name if i<4 else "hard"}',f'tellraw @a {{text:"[Infernal] {name.upper()}",color:"gold"}}','function infernal:scan'])
fn('menu',['tellraw @s '+json.dumps([{'text':'[Infernal] 난이도 선택\n','color':'gold'}]+[{'text':n.upper()+'\n','color':'red' if i>3 else 'white','click_event':{'action':'run_command','command':'/function infernal:set/'+n}} for i,n in enumerate(names)],ensure_ascii=False)])
fn('status',['tellraw @s [{text:"[Infernal] level 0..7: "},{score:{name:"#level",objective:"inf.sys"}}]'])
fn('tick',['scoreboard players add #clock inf.sys 1','execute if score #clock inf.sys matches 10.. run function infernal:pulse'])
fn('pulse',['scoreboard players set #clock inf.sys 0','execute if score #level inf.sys matches 4.. run difficulty hard','function infernal:scan'])
fn('scan',[f'execute in minecraft:{d} as @e[type=#infernal:eligible,tag=!infernal.exclude] unless score @s inf.rev = #epoch inf.sys run function infernal:update' for d in ['overworld','the_nether','the_end']])
fn('context',['execute store result storage infernal:ctx id int 1 run scoreboard players get @s inf.id'])
fn('update',['execute if entity @s[tag=inf.active] run function infernal:restore','scoreboard players operation @s inf.rev = #epoch inf.sys','execute if score #level inf.sys matches ..3 run return 0',
 'execute unless score @s inf.id matches 1.. run function infernal:identify','function infernal:context','function infernal:snapshot with storage infernal:ctx',
 'execute store result score #oldhp inf.sys run data get entity @s Health 100','execute store result score #oldmax inf.sys run attribute @s minecraft:max_health get 100',
 *[f'execute if score #level inf.sys matches {i} run function infernal:apply/{n}' for i,n in enumerate(names) if i>=4],
 'tag @s add inf.active','function infernal:health'])
fn('identify',['scoreboard players add #serial inf.sys 1','scoreboard players operation @s inf.id = #serial inf.sys'])
fn('snapshot',['$data modify storage infernal:backup mobs."$(id)" set value {equipment:{},drop_chances:{}}','$data modify storage infernal:backup mobs."$(id)".equipment set from entity @s equipment','$data modify storage infernal:backup mobs."$(id)".drop_chances set from entity @s drop_chances','$data modify storage infernal:backup mobs."$(id)".fuse set from entity @s Fuse'])
fn('health',['execute store result score #newmax inf.sys run attribute @s minecraft:max_health get 100','scoreboard players set #scale inf.sys 1000','scoreboard players operation #oldhp inf.sys *= #scale inf.sys','scoreboard players operation #oldhp inf.sys /= #oldmax inf.sys','scoreboard players operation #oldhp inf.sys *= #newmax inf.sys','scoreboard players operation #oldhp inf.sys /= #scale inf.sys','execute store result entity @s Health float 0.01 run scoreboard players get #oldhp inf.sys'])
attrs=['max_health','attack_damage','movement_speed','follow_range']
fn('restore',['execute store result score #oldhp inf.sys run data get entity @s Health 100','execute store result score #oldmax inf.sys run attribute @s minecraft:max_health get 100',
 *[f'execute if data entity @s attributes[{{id:"minecraft:{a}"}}].modifiers[{{id:"infernal:{a}"}}] run attribute @s minecraft:{a} modifier remove infernal:{a}' for a in attrs],
 'function infernal:context','function infernal:restore_data with storage infernal:ctx','function infernal:health','tag @s remove inf.gear','tag @s remove inf.active'])
fn('restore_data',['$execute if entity @s[tag=inf.gear] run data modify entity @s equipment set from storage infernal:backup mobs."$(id)".equipment','$execute if entity @s[tag=inf.gear] run data modify entity @s drop_chances set from storage infernal:backup mobs."$(id)".drop_chances','$execute if entity @s[type=minecraft:creeper] run data modify entity @s Fuse set from storage infernal:backup mobs."$(id)".fuse','$data remove storage infernal:backup mobs."$(id)"'])
configs=[(1.2,1.15,1,1.1,10,5,0,1,0,30),(1.4,1.3,1.03,1.2,20,10,10,2,1,30),(1.6,1.5,1.05,1.3,30,15,20,3,2,25),(2,1.8,1.1,1.5,50,35,40,4,3,20)]
def modifier(a,v):return f'attribute @s minecraft:{a} modifier add infernal:{a} {v-1:.5f} add_multiplied_total'
for i,c in enumerate(configs,4):
    hp,atk,speed,follow,armor,weapon,bow,parts,ench,fuse=c;n=names[i]
    lines=[f'execute if entity @s[type=#infernal:ordinary] run {modifier("max_health",hp)}',f'execute if entity @s[type=#infernal:melee] run {modifier("attack_damage",atk)}']
    if speed!=1:lines += [f'execute if entity @s[type=#infernal:melee] unless entity @s[nbt={{IsBaby:1b}}] run {modifier("movement_speed",speed)}']
    lines += ['scoreboard players set #range inf.sys 0',f'execute if entity @s[type=#infernal:ordinary] store result score #range inf.sys run attribute @s minecraft:follow_range get 100',f'execute if entity @s[type=#infernal:ordinary] if score #range inf.sys matches 1.. run {modifier("follow_range",follow)}','execute if entity @s[type=#infernal:ordinary] store result score #range inf.sys run attribute @s minecraft:follow_range get 100','execute if score #range inf.sys matches 6401.. run function infernal:cap_range']
    if i==7:lines += [f'execute if entity @s[type=#infernal:boss] run {modifier("max_health",1.5)}']
    lines += [f'execute if entity @s[type=minecraft:creeper] run data merge entity @s {{Fuse:{fuse}s}}',f'execute if entity @s[type=#infernal:armor] run function infernal:gear/{n}']
    fn('apply/'+n,lines)
    gear=['execute store result score #roll inf.sys run random value 1..100',f'execute if score #roll inf.sys matches ..{armor} run function infernal:armor/{n}','execute store result score #roll inf.sys run random value 1..100',f'execute if entity @s[type=#infernal:zombie] if score #roll inf.sys matches ..{weapon} unless data entity @s equipment.mainhand.id run function infernal:weapon/{n}']
    if bow:gear+=['execute store result score #roll inf.sys run random value 1..100',f'execute if entity @s[type=#infernal:archer] if score #roll inf.sys matches ..{bow} if data entity @s equipment.mainhand{{id:"minecraft:bow"}} unless data entity @s equipment.mainhand.components."minecraft:enchantments" run function infernal:bow/{n}']
    fn('gear/'+n,gear)
    def give(slot,item,level=0,enchantment='protection'):
        comp=',components:{"minecraft:enchantments":{"minecraft:'+enchantment+'":'+str(level)+'}}' if level else ''
        return [f'data modify entity @s equipment.{slot} set value {{id:"minecraft:{item}",count:1{comp}}}',f'data modify entity @s drop_chances.{slot} set value 0.0f','tag @s add inf.gear']
    ar=['execute store result score #parts inf.sys run random value '+('1..1' if i==4 else f'{2 if i>=6 else 1}..{parts}')]
    # Random slot order permits 1-4 independent empty slots without replacing natural gear.
    ar+=['execute store result score #order inf.sys run random value 0..3']
    slots=['feet','legs','chest','head'];items=['boots','leggings','chestplate','helmet']
    for order in range(4):
        sub=[]
        for j in range(parts):
            k=(j+order)%4;slot=slots[k];sub += [f'execute if score #parts inf.sys matches {j+1}.. unless data entity @s equipment.{slot}.id run function infernal:piece/{n}_{slot}']
        fn(f'armor/{n}_{order}',sub);ar += [f'execute if score #order inf.sys matches {order} run function infernal:armor/{n}_{order}']
    fn('armor/'+n,ar)
    for slot,item in zip(slots,items):
        piece=['execute store result score #material inf.sys run random value 1..100','execute store result score #enchant inf.sys run random value 1..100']
        materials=[('leather',50),('chainmail',100)] if i==4 else [('chainmail',75 if i==5 else 40),('iron',100)] if i<7 else [('iron',100)]
        low=1
        for material,high in materials:
            key=f'piece/{n}_{slot}_{material}';fn(key,give(slot,material+'_'+item))
            piece += [f'execute if score #material inf.sys matches {low}..{high} run function infernal:{key}'];low=high+1
        if ench:
            fn(f'piece/{n}_{slot}_ench',[f'data modify entity @s equipment.{slot}.components."minecraft:enchantments" set value {{"minecraft:protection":{ench}}}'])
            piece += [f'execute if score #enchant inf.sys matches ..40 run function infernal:piece/{n}_{slot}_ench']
        if i==7 and slot=='chest':
            fn('piece/nightmare_diamond',give(slot,'diamond_chestplate',2));piece+=['execute if score #material inf.sys matches ..5 run function infernal:piece/nightmare_diamond']
        fn(f'piece/{n}_{slot}',piece)
    weaponitem='iron_shovel' if i==4 else 'iron_sword'
    wl=give('mainhand',weaponitem,2 if i==7 else 1 if i==6 else 0,'sharpness')
    if i==7:
        fn('weapon/nightmare_diamond',give('mainhand','diamond_sword',2,'sharpness'))
        wl+=['execute store result score #rare inf.sys run random value 1..100','execute if score #rare inf.sys matches ..5 run function infernal:weapon/nightmare_diamond']
    fn('weapon/'+n,wl)
    fn('bow/'+n,give('mainhand','bow',max(1,ench),'power'))
fn('cap_range',['attribute @s minecraft:follow_range modifier remove infernal:follow_range','execute store result score #base inf.sys run attribute @s minecraft:follow_range get 100','scoreboard players set #cap inf.sys 6400','scoreboard players operation #cap inf.sys -= #base inf.sys','execute store result storage infernal:ctx cap double 0.01 run scoreboard players get #cap inf.sys','function infernal:cap_add with storage infernal:ctx'])
fn('cap_add',['$attribute @s minecraft:follow_range modifier add infernal:follow_range $(cap) add_value'])
fn('uninstall',['function infernal:set/hard','tellraw @a {text:"[Infernal] Hard로 복원됨. 미로딩 청크의 몹 복원을 위해 팩을 유지하고 지역을 방문하세요. README 참고.",color:"yellow"}'])
out=BASE/'output';out.mkdir(exist_ok=True)
zpath=out/'Infernal-Difficulties-26.3.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(PACK.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(PACK).as_posix())
    if (BASE/'README.ko.md').exists():z.write(BASE/'README.ko.md','README.ko.md')
js(out/'SHA256.json',{zpath.name:hashlib.sha256(zpath.read_bytes()).hexdigest()})
print(zpath)
