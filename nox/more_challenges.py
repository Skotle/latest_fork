"""Normal progression and per-encounter hard challenges with explicit counters."""
from build import DP,NS,OUT,fn,js,call
from expansion import read,add
import json

def upgrade_more_challenges():
    root=DP/f'data/{NS}/advancement/challenge'
    p=root/'victory.json';d=json.loads(p.read_text());d['display']['description']={'text':'녹스를 처음 처치하기 — 승리 시 보상을 받는 참가자에게 지급'};d['display']['frame']='goal';d['display']['announce_to_chat']=False;js(p,d)
    nodes=[
      ('discover','잊힌 관측소','오버월드 지하 일식 관측소에 접근하기','compass','root','task'),
      ('pair','두 종의 잔향','한 전투에서 시종과 파수꾼을 각각 직접 처치하기','golden_apple','warden','goal'),
      ('veteran','종지기의 기록','녹스 처치에 총 3회 성공하기','diamond','victory','goal'),
      ('no_acolyte','거두지 않은 잔향','팀이 시종을 한 마리도 직접 처치하지 않고 녹스 처치하기','wither_rose','victory','challenge'),
      ('no_adds','종지기만 쓰러뜨려라','팀이 시종과 파수꾼을 한 마리도 직접 처치하지 않고 녹스 처치하기','soul_lantern','no_acolyte','challenge'),
      ('solo','홀로 맞선 일식','참가자가 1명인 전투에서 녹스 처치하기','diamond_sword','victory','challenge'),
      ('speed','종이 멎기 전에','전투 시작부터 3분 이내에 녹스 처치하기','clock','victory','challenge'),
      ('pure_seal','한 치의 오음도 없이','팀이 봉인종 순서 실수와 과부하 없이 봉인을 해제한 전투에서 승리하기','amethyst_block','seal','challenge'),
      ('trials','세 번의 심판','한 전투에서 최후의 심판을 3회 피하고 승리하기','totem_of_undying','judgement','challenge'),
      ('counter_master','반격의 지배자','한 전투에서 서로 다른 노출 기회 3회에 직접 반격하고 승리하기','netherite_sword','counter','challenge')]
    for name,title,desc,icon,parent,frame in nodes:
        js(root/f'{name}.json',{'parent':f'{NS}:challenge/{parent}','display':{'icon':{'id':'minecraft:'+icon},'title':{'text':title},'description':{'text':desc},'frame':frame,'show_toast':True,'announce_to_chat':frame=='challenge','hidden':False},'criteria':{'earned':{'trigger':'minecraft:impossible'}}})
    add('fight/begin',['scoreboard players set #team_acolyte nx.acolyte 0','scoreboard players set #team_adds nx.warden 0'])
    add('minions/reward_acolyte',['execute if score #state nx.state matches 1 if entity @s[tag=nox.member] run scoreboard players set #team_acolyte nx.acolyte 1','execute if score #state nx.state matches 1 if entity @s[tag=nox.member] run scoreboard players set #team_adds nx.warden 1'])
    add('minions/reward_warden',['execute if score #state nx.state matches 1 if entity @s[tag=nox.member] run scoreboard players set #team_adds nx.warden 1'])
    add('load',[f'scoreboard objectives add nx.{name} dummy' for name in ['wins','acolyte','warden','trials','counter','window']])
    add('tick_overworld',[f'execute as @e[tag=nox.anchor] at @s run advancement grant @a[distance=..38,gamemode=!spectator] only {NS}:challenge/discover'])
    add('fight/begin',['scoreboard players set #window nx.window 0','scoreboard players set #mistakes nx.tmp 0','scoreboard players set #sealclean nx.tmp 0',
        'execute store result score #party nx.tmp if entity @a[tag=nox.member]',
        'execute as @a[tag=nox.member] run '+call('challenge/reset_run')])
    fn('challenge/reset_run',['scoreboard players add @s nx.wins 0']+[f'scoreboard players set @s nx.{name} 0' for name in ['acolyte','warden','trials','counter']]+['scoreboard players set @s nx.window -1'])
    for kind in ['acolyte','warden']:
        add('minions/boon_'+kind,[f'execute if entity @s[type=minecraft:player,tag=nox.active] run scoreboard players add @s nx.{kind} 1',
            f'execute if entity @s[type=minecraft:player,tag=nox.active] if score @s nx.acolyte matches 1.. if score @s nx.warden matches 1.. run advancement grant @s only {NS}:challenge/pair'])
    for name in ['skills/dash/counter','minions/break']:
        add(name,['scoreboard players add #window nx.window 1'])
    bonus=read('fight/bonus');bonus=[l for l in bonus if 'challenge/counter' not in l];fn('fight/bonus',bonus)
    fn('challenge/counter_credit',[f'advancement grant @s only {NS}:challenge/counter',call('challenge/count_counter')])
    js(DP/f'data/{NS}/advancement/internal/counter_hit.json',{'criteria':{'hit':{'trigger':'minecraft:player_hurt_entity','conditions':{'entity':{'type':'minecraft:entity_properties','entity':'this','predicate':{'minecraft:nbt':'{Tags:["nox.boss"]}'}},'damage':{'taken':{'min':0.001}}}}},'rewards':{'function':f'{NS}:challenge/counter_hit'}})
    fn('challenge/counter_hit',[f'advancement revoke @s only {NS}:internal/counter_hit',
        'execute if score #state nx.state matches 1 if score #counter nx.move matches 1 if score #safe nx.safe matches 1.. if entity @s[tag=nox.active] run '+call('challenge/counter_credit')])
    fn('challenge/count_counter',['execute unless score @s nx.window = #window nx.window run scoreboard players add @s nx.counter 1','scoreboard players operation @s nx.window = #window nx.window'])
    lines=read('judgement/resolve');idx=next(i for i,l in enumerate(lines) if 'challenge/judgement' in l);lines.insert(idx,'scoreboard players add @a[tag=nox.active,tag=nox.doom_safe] nx.trials 1');fn('judgement/resolve',lines)
    # Remember mistakes before temporary puzzle variables are updated or reset.
    add('puzzle/press',['execute unless score #bell nx.tmp = #expected nx.tmp run scoreboard players add #mistakes nx.tmp 1'])
    add('puzzle/overload',['scoreboard players add #mistakes nx.tmp 1'])
    add('puzzle/success',['execute if score #mistakes nx.tmp matches 0 run scoreboard players set #sealclean nx.tmp 1'])
    add('reward',[call('challenge/win')])
    fn('challenge/win',['scoreboard players add @s nx.wins 1',
        f'execute if score #team_acolyte nx.acolyte matches 0 run advancement grant @s only {NS}:challenge/no_acolyte',
        f'execute if score #team_adds nx.warden matches 0 run advancement grant @s only {NS}:challenge/no_adds',
        f'execute if score @s nx.wins matches 3.. run advancement grant @s only {NS}:challenge/veteran',
        f'execute if score #party nx.tmp matches 1 run advancement grant @s only {NS}:challenge/solo',
        f'execute if score #time nx.time matches ..3600 run advancement grant @s only {NS}:challenge/speed',
        f'execute if score #sealclean nx.tmp matches 1 run advancement grant @s only {NS}:challenge/pure_seal',
        f'execute if score @s nx.trials matches 3.. run advancement grant @s only {NS}:challenge/trials',
        f'execute if score @s nx.counter matches 3.. run advancement grant @s only {NS}:challenge/counter_master'])
    profile=json.loads((OUT/'timing-profile.json').read_text());profile.update(advancements=18,normal_advancements=10,hard_advancements=8);js(OUT/'timing-profile.json',profile)
    js(OUT/'challenge-guide.json',{'normal':['지하의 종소리','잊힌 관측소','깨진 봉인','잔향을 거두다','종을 부수다','균형을 무너뜨려라','심판의 중심','일식을 걷어내다','두 종의 잔향','종지기의 기록'],
        'hard':['거두지 않은 잔향 — 팀이 시종 직접 처치 없이 승리','종지기만 쓰러뜨려라 — 팀이 하위 몹 직접 처치 없이 승리','완벽한 종지기 — 무피해 승리','홀로 맞선 일식 — 1인 승리','종이 멎기 전에 — 3분 이내 승리','한 치의 오음도 없이 — 봉인종 실수·과부하 없는 팀 승리','세 번의 심판 — 심판 3회 생존 후 승리','반격의 지배자 — 서로 다른 노출 3회 반격 후 승리'],
        'reset':'Failed runs do not carry run counters into a new encounter; lifetime wins and earned advancements persist.'})
