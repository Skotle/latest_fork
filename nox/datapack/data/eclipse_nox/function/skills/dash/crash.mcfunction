scoreboard players set #dash nx.dash 0
scoreboard players set #crash nx.move 1
execute at @e[tag=nox.boss,limit=1] run particle minecraft:explosion ~ ~1 ~ .8 .4 .8 0 12 force @a[tag=nox.member]
