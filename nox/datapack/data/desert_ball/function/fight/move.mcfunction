execute facing entity @a[tag=db.active,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score #skill db.skill matches 4 if score #cast db.cast matches 24.. positioned ^.24 ^ ^ if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air if entity @e[tag=db.anchor,tag=db.current,distance=..28] run tp @s ~ ~ ~
execute if score #skill db.skill matches 4 if score #cast db.cast matches ..23 positioned ^-.24 ^ ^ if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air if entity @e[tag=db.anchor,tag=db.current,distance=..28] run tp @s ~ ~ ~
execute unless score #skill db.skill matches 4 if entity @a[tag=db.active,distance=..10] positioned ^ ^ ^-.18 if block ~ ~ ~ minecraft:air if entity @e[tag=db.anchor,tag=db.current,distance=..28] run tp @s ~ ~ ~
