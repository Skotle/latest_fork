$execute if score @s ida.skill matches 0 run function dungeons_arise:boss/spell/$(primary)/hit with entity @s data
$execute if score @s ida.skill matches 1 run function dungeons_arise:boss/spell/$(secondary)/hit with entity @s data
$kill @e[tag=ida.target,scores={ida.sid=$(id)}]
scoreboard players set @s ida.stage 0
scoreboard players add @s ida.skill 1
execute if score @s ida.skill matches 2.. run scoreboard players set @s ida.skill 0
