scoreboard players remove #dash nx.dash 1
scoreboard players set #moved nx.move 0
execute as @e[tag=nox.boss,limit=1] at @s rotated as @e[tag=nox.target,limit=1] positioned ^ ^ ^.8 if entity @e[tag=nox.anchor,tag=nox.current,distance=..21,limit=1] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air store success score #moved nx.move run tp @s ~ ~ ~ ~ 0
execute as @e[tag=nox.boss,limit=1] at @s run particle minecraft:cloud ~ ~.3 ~ .4 .2 .4 .02 10 force @a[tag=nox.member]
execute as @e[tag=nox.boss,limit=1] at @s as @a[tag=nox.active,tag=!nox.dashhit,distance=..2.7] run function eclipse_nox:damage/dash
execute if score #moved nx.move matches 0 run function eclipse_nox:skills/dash/crash
execute at @e[tag=nox.anchor,tag=nox.current,limit=1] as @e[tag=nox.boss,limit=1] unless entity @s[distance=..21] run function eclipse_nox:skills/dash/crash
execute if score #dash nx.dash matches 0 run function eclipse_nox:skills/dash/end
