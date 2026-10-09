kill @e[tag=fw.vector]
summon minecraft:marker ~ ~ ~ {Tags:["fw.vector"]}
execute store result score #x fw.tmp run data get entity @e[tag=fw.vector,limit=1] Pos[0] 1000
execute store result score #y fw.tmp run data get entity @e[tag=fw.vector,limit=1] Pos[1] 1000
execute store result score #z fw.tmp run data get entity @e[tag=fw.vector,limit=1] Pos[2] 1000
execute positioned ^ ^ ^1 run tp @e[tag=fw.vector,limit=1] ~ ~ ~
execute store result score #vx fw.tmp run data get entity @e[tag=fw.vector,limit=1] Pos[0] 1000
scoreboard players operation #vx fw.tmp -= #x fw.tmp
execute store result storage frost_warden:shot vx double 0.0020 run scoreboard players get #vx fw.tmp
execute store result score #vy fw.tmp run data get entity @e[tag=fw.vector,limit=1] Pos[1] 1000
scoreboard players operation #vy fw.tmp -= #y fw.tmp
execute store result storage frost_warden:shot vy double 0.0020 run scoreboard players get #vy fw.tmp
execute store result score #vz fw.tmp run data get entity @e[tag=fw.vector,limit=1] Pos[2] 1000
scoreboard players operation #vz fw.tmp -= #z fw.tmp
execute store result storage frost_warden:shot vz double 0.0020 run scoreboard players get #vz fw.tmp
data modify storage frost_warden:shot owner set from storage frost_warden:ctx owner
function frost_warden:arrows/summon with storage frost_warden:shot
function frost_warden:arrows/register
kill @e[tag=fw.vector]
