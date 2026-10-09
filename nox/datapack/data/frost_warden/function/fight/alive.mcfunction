scoreboard players add #time fw.time 1
execute store result score #hp fw.hp run data get entity @e[tag=fw.boss,limit=1] Health 100
scoreboard players operation #loss fw.hp = #last fw.hp
scoreboard players operation #loss fw.hp -= #hp fw.hp
execute if score #loss fw.hp matches 1.. run scoreboard players operation #pool fw.hp -= #loss fw.hp
execute if score #pool fw.hp matches ..0 run return run function frost_warden:victory
data merge entity @e[tag=fw.boss,limit=1] {Health:1000f}
scoreboard players set #last fw.hp 100000
scoreboard players operation #hp fw.hp = #pool fw.hp
scoreboard players operation #ratio fw.tmp = #hp fw.hp
scoreboard players operation #ratio fw.tmp /= #max fw.max
execute if score #phase fw.phase matches 1 if score #ratio fw.tmp matches ..70 run function frost_warden:phase/two
execute if score #phase fw.phase matches 2 if score #ratio fw.tmp matches ..35 run function frost_warden:phase/three
scoreboard players operation #bar fw.hp = #pool fw.hp
scoreboard players operation #bar fw.hp /= #hundred fw.tmp
execute store result bossbar frost_warden:health value run scoreboard players get #bar fw.hp
execute store result bossbar frost_warden:health max run scoreboard players get #max fw.max
execute as @e[tag=fw.add,nbt={Health:0.0f}] at @s run function frost_warden:adds/death
execute if score #safe fw.safe matches 1.. run scoreboard players remove #safe fw.safe 1
execute if score #cast fw.cast matches 1.. run function frost_warden:skills/casting
execute if score #cast fw.cast matches 0 if score #safe fw.safe matches 0 run scoreboard players remove #next fw.next 1
execute if score #cast fw.cast matches 0 if score #safe fw.safe matches 0 if score #next fw.next matches ..0 if entity @a[tag=fw.active,gamemode=!creative] run function frost_warden:skills/begin
function frost_warden:arrows/native with storage frost_warden:ctx
execute as @e[tag=fw.arrow] at @s run function frost_warden:arrows/tick
execute as @e[tag=fw.add] run function frost_warden:arrows/add_scan
execute as @e[tag=fw.tracker] at @s run function frost_warden:arrows/tracker
execute as @e[tag=fw.bomb_mark] at @s run function frost_warden:bomb/tick
function frost_warden:teleport/tick
execute as @a[tag=fw.active,tag=fw.stunned] run function frost_warden:debuff/tick
execute if score #cast fw.cast matches 0 if score #safe fw.safe matches 0 run data merge entity @e[tag=fw.boss,limit=1] {NoAI:0b}
execute as @a[tag=fw.active,scores={fw.guard=1..}] run scoreboard players remove @s fw.guard 1
execute as @e[tag=fw.hawk] at @s run function frost_warden:ashe/hawk_tick
