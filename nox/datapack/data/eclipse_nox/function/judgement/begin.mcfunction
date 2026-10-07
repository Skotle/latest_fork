scoreboard players set #judgement nx.doom 40
scoreboard players set #doom nx.doom 160
scoreboard players set #cast nx.cast 41
scoreboard players set #skill nx.skill 6
scoreboard players set #total nx.total 41
tellraw @a[tag=nox.member] {"text": "최후의 심판! 2초 안에 중앙 금빛 원으로 들어오세요!", "color": "gold"}
playsound minecraft:entity.wither.spawn master @a[tag=nox.member] ~ ~ ~ .6 1.5
