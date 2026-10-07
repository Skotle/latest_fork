scoreboard players operation #frame ida.tmp = #clock ida.tick
scoreboard players set #five ida.tmp 5
scoreboard players operation #frame ida.tmp /= #five ida.tmp
scoreboard players remove #frame ida.tmp 1
execute if score #frame ida.tmp matches ..-1 run scoreboard players set #frame ida.tmp 0
execute store result entity @s data.frame int 1 run scoreboard players get #frame ida.tmp
execute store result entity @s data.visual_phase int 1 run scoreboard players get @s ida.phase
data modify entity @s data.pose set value "idle"
execute store result score #vx ida.tmp run data get entity @s Motion[0] 1000
execute store result score #vz ida.tmp run data get entity @s Motion[2] 1000
execute unless score #vx ida.tmp matches -5..5 run data modify entity @s data.pose set value "walk"
execute unless score #vz ida.tmp matches -5..5 run data modify entity @s data.pose set value "walk"
execute if score @s ida.stage matches 1 run data modify entity @s data.pose set value "wind"
execute if score @s ida.stage matches 2 run data modify entity @s data.pose set value "recover"
function dungeons_arise:boss/visual/pose with entity @s data
