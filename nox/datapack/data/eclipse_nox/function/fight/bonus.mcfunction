scoreboard players operation #lost nx.hp = #oldhp nx.hp
scoreboard players operation #lost nx.hp -= #seen nx.hp
scoreboard players set #two nx.tmp 2
execute if score #counter nx.move matches 1 run scoreboard players set #two nx.tmp 1
scoreboard players operation #lost nx.hp /= #two nx.tmp
scoreboard players operation #seen nx.hp -= #lost nx.hp
execute if score #seen nx.hp matches 1.. store result storage eclipse_nox:damage health double .01 run scoreboard players get #seen nx.hp
execute if score #seen nx.hp matches 1.. run function eclipse_nox:fight/set_health with storage eclipse_nox:damage
execute if score #seen nx.hp matches ..0 run kill @e[tag=nox.boss]
execute at @e[tag=nox.boss,limit=1] run particle minecraft:crit ~ ~1.8 ~ .6 .5 .6 .1 12 force @a[tag=nox.member]
