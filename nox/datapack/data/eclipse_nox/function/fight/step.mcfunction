execute if entity @a[tag=nox.active,distance=4..,limit=1] positioned ^ ^ ^.16 if entity @e[tag=nox.anchor,tag=nox.current,distance=..21,limit=1] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~ ~ 0
execute if entity @a[tag=nox.active,distance=..3,limit=1] positioned ^.06 ^ ^-.03 if entity @e[tag=nox.anchor,tag=nox.current,distance=..21,limit=1] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~ ~ 0
execute if entity @a[tag=nox.active,limit=1] run scoreboard players set #moving nx.move 1
