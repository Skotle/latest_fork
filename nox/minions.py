"""Articulated minions, restrained reinforcements and player-earned death boons."""
import json,math
from build import DP,RP,NS,OUT,fn,js,call,display
from expansion import read,add
from motion import quaternion,snbt

def upgrade_minions():
    add('load',['scoreboard objectives add nx.mx dummy','scoreboard objectives add nx.mz dummy','scoreboard objectives add nx.mid dummy'])
    for name in ['fight/begin','fight/cleanup']:
        add(name,['scoreboard players set #break nx.add 0'])
    # First pair only; later phases do not create additional waves on transition.
    for name in ['fight/phase2','fight/phase3']:
        fn(name,[l for l in read(name) if l!=call('minions/spawn')])
    # Native visible mobs provide their own model, animation and hitbox.
    for kind,entity in [('acolyte','husk'),('warden','zombie')]:
        content=read('minions/spawn_'+kind)[0]
        mob=json.loads(content.split(' ~ ~ ~ ',1)[1])
        mob.pop('Passengers',None);mob.pop('active_effects',None)
        mob['Invulnerable']=False;mob['CanPickUpLoot']=False;mob['DeathLootTable']='minecraft:empty'
        mob['attributes']=[v for v in mob['attributes'] if v['id']!='minecraft:scale']
        mob['CustomName']={'text':'잔향 시종' if kind=='acolyte' else '종의 파수꾼','color':'aqua' if kind=='acolyte' else 'gold'}
        fn('minions/spawn_'+kind,['summon minecraft:'+entity+' ~ ~ ~ '+json.dumps(mob,separators=(',',':'))])
    # Remove only our former minion assets; the boss and original pack stay intact.
    for folder in ['models','items']:
        for asset in (RP/f'assets/{NS}/{folder}').glob('*.json'):
            if asset.stem in ['acolyte','warden'] or asset.stem.startswith(('acolyte_','warden_')): asset.unlink()
    for kind in ['acolyte','warden']:
        (RP/f'assets/{NS}/textures/entity/{kind}.png').unlink(missing_ok=True)
    atlas_path=RP/'assets/minecraft/atlases/items.json'
    atlas=json.loads(atlas_path.read_text());atlas['sources']=[v for v in atlas['sources'] if v.get('resource') not in [f'{NS}:entity/acolyte',f'{NS}:entity/warden']];js(atlas_path,atlas)
    for asset in (DP/f'data/{NS}/function/minions').rglob('*.mcfunction'):
        if asset.relative_to(DP/f'data/{NS}/function/minions').parts[0]=='pose' or asset.stem in ['animate','select','follow','bind_acolyte','bind_warden']:asset.unlink()
    fn('minions/spawn',['execute positioned ~-10 ~ ~-8 run '+call('minions/spawn_acolyte'),'execute positioned ~10 ~ ~8 run '+call('minions/spawn_warden')])
    fn('minions/reinforce',['scoreboard players set #adds nx.add 0',call('minions/spawn')])
    fn('minions/tick',[
        'execute as @e[tag=nox.minion] at @s run '+call('minions/entity_tick'),
        'tag @e[tag=nox.minion_visual] remove nox.riding','kill @e[tag=nox.minion_visual,tag=!nox.riding]',
        'scoreboard players add #adds nx.add 1','execute if score #adds nx.add matches 1200.. run '+call('minions/reinforce'),
        'execute if score #break nx.add matches 1 if score #cast nx.cast matches 0 if score #dash nx.dash matches 0 if score #puzzle nx.puzzle matches 0 if score #safe nx.safe matches 0 run '+call('minions/break')])
    (DP/f'data/{NS}/function/minions/retire.mcfunction').unlink(missing_ok=True)
    fn('minions/entity_tick',[
        'execute store result score @s nx.hp run data get entity @s Health 100',
        'execute if score @s nx.hp matches ..0 unless entity @s[tag=nox.paid] run '+call('minions/death'),
        'execute unless entity @e[tag=nox.anchor,tag=nox.current,distance=..24] at @e[tag=nox.anchor,tag=nox.current,limit=1] run tp @s ~ ~ ~'])
    fn('minions/death',['tag @s add nox.paid','scoreboard players operation #carrier nx.mid = @s nx.mid','execute as @e[tag=nox.minion_visual] if score @s nx.mid = #carrier nx.mid run kill @s'])
    # Death rewards use the engine kill event: dead carriers can vanish from selectors.
    for kind in ['acolyte','warden']:
        js(DP/f'data/{NS}/advancement/minions/kill_{kind}.json',{'criteria':{'kill':{'trigger':'minecraft:player_killed_entity','conditions':{'entity':{'type':'minecraft:entity_properties','entity':'this','predicate':{'minecraft:entity_type':'minecraft:husk' if kind=='acolyte' else 'minecraft:zombie','minecraft:nbt':'{Tags:["nox.minion","nox.add.'+kind+'"]}'}}}}},'rewards':{'function':f'{NS}:minions/reward_{kind}'}})
        fn('minions/reward_'+kind,[f'advancement revoke @s only {NS}:minions/kill_{kind}',
            'execute if score #state nx.state matches 1 if entity @s[tag=nox.active] at @s run '+call('minions/boon_'+kind)])
    fn('minions/boon_acolyte',[
        'effect give @a[tag=nox.active,distance=..8] minecraft:instant_health 1 0 true',
        'effect give @a[tag=nox.active,distance=..8] minecraft:regeneration 5 0 true',
        'effect give @a[tag=nox.active,distance=..8] minecraft:speed 5 0 true',
        'particle minecraft:heart ~ ~1 ~ 2 .5 2 0 14 force @a[tag=nox.member]',
        'tellraw @a[tag=nox.active,distance=..8] {"text":"시종의 잔향: 체력 회복 + 5초 재생·신속!","color":"aqua"}'])
    fn('minions/boon_warden',[
        'effect give @a[tag=nox.active,distance=..8] minecraft:resistance 6 0 true',
        'effect give @a[tag=nox.active,distance=..8] minecraft:absorption 6 0 true',
        'scoreboard players set #break nx.add 1',
        'particle minecraft:totem_of_undying ~ ~1 ~ 2 .5 2 .1 18 force @a[tag=nox.member]',
        'tellraw @a[tag=nox.member] {"text":"파수꾼의 종 파괴: 6초 저항·흡수. 다음 공격 종료 후 녹스 심장 2초 노출!","color":"gold"}'])
    fn('minions/break',['scoreboard players set #break nx.add 0','scoreboard players set #safe nx.safe 40','scoreboard players set #next nx.next 0','scoreboard players set #expose nx.expose 1','scoreboard players set #counter nx.move 1',
        'execute store result score #oldhp nx.hp run data get entity @e[tag=nox.boss,limit=1] Health 100',
        'tellraw @a[tag=nox.member] {"text":"파수꾼의 반격: 녹스에게 주는 피해 2배, 2초!","color":"gold"}'])
    profile=json.loads((OUT/'timing-profile.json').read_text());profile.update(minion_cap=None,minion_reinforcement_ticks=1200,minion_lifetime_ticks=None,minion_refill_only_when_empty=False,minion_joints=0,minion_visuals='vanilla_husk_and_zombie',minion_carrier_scale=1.0);js(OUT/'timing-profile.json',profile)
