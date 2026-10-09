execute at @e[tag=fw.boss,limit=1] run particle minecraft:portal ~ ~1 ~ .4 .7 .4 .05 40 force @a[tag=fw.active]
execute at @e[tag=fw.destination,sort=random,limit=1] run tp @e[tag=fw.boss,limit=1] ~ ~ ~
execute as @e[tag=fw.boss,limit=1] at @s facing entity @a[tag=fw.active,sort=nearest,limit=1] eyes run tp @s ~ ~ ~ ~ ~
execute at @e[tag=fw.boss,limit=1] run particle minecraft:snowflake ~ ~1 ~ .5 .7 .5 .03 35 force @a[tag=fw.active]
execute at @e[tag=fw.boss,limit=1] run playsound minecraft:entity.enderman.teleport hostile @a[tag=fw.active] ~ ~ ~ .8 1.4
scoreboard players add #teleports fw.tmp 1
