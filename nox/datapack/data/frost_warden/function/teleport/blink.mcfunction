tag @e[tag=fw.teleport_point] remove fw.destination
execute at @e[tag=fw.boss,limit=1] as @e[tag=fw.teleport_point,distance=6..] at @s if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air unless block ~ ~-1 ~ #frost_warden:blast_pass unless entity @a[tag=fw.active,distance=..3] run tag @s add fw.destination
execute if entity @e[tag=fw.destination] run function frost_warden:teleport/move
scoreboard players set #blink fw.blink 200
