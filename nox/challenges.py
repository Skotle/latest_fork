"""Encounter advancement tree and harder pacing while retaining counterplay."""
import json
from build import DP,NS,OUT,fn,js,call
from expansion import add,read
from timing import patch

def upgrade_challenges():
    nodes=[('root','지하의 종소리','녹스와의 전투에 참가하기','bell',None,'task'),
        ('seal','깨진 봉인','참가 중 봉인종 퍼즐을 해결한 팀에 남아 있기','amethyst_shard','root','task'),
        ('acolyte','잔향을 거두다','시종을 직접 처치해 회복 효과 얻기','glow_berries','root','task'),
        ('warden','종을 부수다','파수꾼을 직접 처치해 반격 기회 만들기','shield','acolyte','goal'),
        ('counter','균형을 무너뜨려라','벽 충돌 또는 파수꾼 노출 중 녹스를 직접 공격하기','iron_sword','root','goal'),
        ('judgement','심판의 중심','최후의 심판 안전 구역 안에서 살아남기','totem_of_undying','counter','goal'),
        ('victory','일식을 걷어내다','죽거나 접속을 끊지 않고 녹스 처치에 성공하기','nether_star','seal','challenge'),
        ('flawless','완벽한 종지기','전투 중 피해를 한 번도 받지 않고 승리하기','enchanted_golden_apple','victory','challenge')]
    for name,title,desc,icon,parent,frame in nodes:
        d={'display':{'icon':{'id':'minecraft:'+icon},'title':{'text':title},'description':{'text':desc},'frame':frame,'show_toast':True,'announce_to_chat':frame=='challenge','hidden':name=='flawless'},'criteria':{'earned':{'trigger':'minecraft:impossible'}}}
        if parent:d['parent']=f'{NS}:challenge/{parent}'
        else:d['display']['background']='minecraft:gui/advancements/backgrounds/adventure'
        js(DP/f'data/{NS}/advancement/challenge/{name}.json',d)
    add('load',['scoreboard objectives add nx.clean dummy'])
    add('fight/begin',['scoreboard players set @a[tag=nox.member] nx.clean 1',f'advancement grant @a[tag=nox.member] only {NS}:challenge/root'])
    add('puzzle/success',[f'advancement grant @a[tag=nox.active] only {NS}:challenge/seal'])
    for kind in ['acolyte','warden']:
        add('minions/boon_'+kind,[f'execute if entity @s[type=minecraft:player,tag=nox.active] run advancement grant @s only {NS}:challenge/{kind}'])
    add('fight/bonus',[f'execute if score #counter nx.move matches 1 as @e[tag=nox.boss,limit=1] on attacker if entity @s[type=minecraft:player,tag=nox.active] run advancement grant @s only {NS}:challenge/counter'])
    judgement=read('judgement/resolve');judgement.insert(2,f'advancement grant @a[tag=nox.active,tag=nox.doom_safe] only {NS}:challenge/judgement');fn('judgement/resolve',judgement)
    add('reward',[f'advancement grant @s only {NS}:challenge/victory',f'execute if score @s nx.clean matches 1 run advancement grant @s only {NS}:challenge/flawless'])
    js(DP/f'data/{NS}/advancement/internal/hurt.json',{'criteria':{'hurt':{'trigger':'minecraft:entity_hurt_player','conditions':{'damage':{'taken':{'min':0.001}}}}},'rewards':{'function':f'{NS}:challenge/hurt'}})
    fn('challenge/hurt',[f'advancement revoke @s only {NS}:internal/hurt','execute if score #state nx.state matches 1 if entity @s[tag=nox.member] run scoreboard players set @s nx.clean 0'])
    patch('fight/begin',[('#max nx.max 300','#max nx.max 450'),('#max nx.max matches 1501..','#max nx.max matches 1801..'),('#max nx.max 1500','#max nx.max 1800')])
    patch('damage/8',[('damage @s 6 minecraft:mob_attack','damage @s 8 minecraft:mob_attack')])
    patch('damage/dash',[('damage @s 7 minecraft:mob_attack','damage @s 9 minecraft:mob_attack')])
    patch('skills/begin',[('#cast nx.cast 20','#cast nx.cast 16'),('#cast nx.cast 16','#cast nx.cast 14')])
    # The previous replace is global: explicitly select the normal cleave/ring to 16.
    begin=read('skills/begin');begin=[l.replace('#cast nx.cast 14','#cast nx.cast 16') if 'matches 5 ' not in l else l for l in begin];fn('skills/begin',begin)
    patch('skills/combo',[('#cast nx.cast 12','#cast nx.cast 10'),('#total nx.total 12','#total nx.total 10')])
    patch('fight/step',[('^ ^ ^.12','^ ^ ^.16')])
    patch('judgement/begin',[('#doom nx.doom 160','#doom nx.doom 120')])
    patch('fight/phase3',[('반경 4블록','반경 3.5블록')])
    patch('judgement/resolve',[('distance=..4]','distance=..3.5]')])
    # Regenerate the perimeter to exactly match the smaller safety radius.
    import math
    p=DP/f'data/{NS}/function/judgement/tick.mcfunction';lines=p.read_text(encoding='utf-8').splitlines()
    index=0
    for i,l in enumerate(lines):
        if 'minecraft:end_rod ' in l:
            a=index*math.tau/40;lines[i]=f'particle minecraft:end_rod ~{math.cos(a)*3.5:.3f} ~.2 ~{math.sin(a)*3.5:.3f} 0 .3 0 0 1 force @a[tag=nox.member]';index+=1
    assert index==40;fn('judgement/tick',lines)
    for kind,hp,speed,attack in [('acolyte',28,.31,4),('warden',42,.25,6)]:
        line=read('minions/spawn_'+kind)[0];prefix,data=line.split(' ~ ~ ~ ',1);mob=json.loads(data);mob['Health']=hp
        for attribute in mob['attributes']:
            if attribute['id']=='minecraft:max_health':attribute['base']=hp
            if attribute['id']=='minecraft:movement_speed':attribute['base']=speed
            if attribute['id']=='minecraft:attack_damage':attribute['base']=attack
        fn('minions/spawn_'+kind,[prefix+' ~ ~ ~ '+json.dumps(mob,separators=(',',':'))])
    profile=json.loads((OUT/'timing-profile.json').read_text());profile['telegraph_ticks'].update(cleave=16,second_cleave=10,dash=14,ring=16);profile.update(judgement_retry_ticks=120,judgement_safe_radius=3.5,boss_health={'solo':900,'two':1350,'three_or_more':1800},melee_damage=8,dash_damage=9,advancements=len(nodes));js(OUT/'timing-profile.json',profile)
