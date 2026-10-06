scoreboard players set @s ida.stage 1
scoreboard players set @s ida.wind 40
scoreboard players set @s ida.cd 0
execute if data entity @s data{primary:"sunfire"} if score @s ida.skill matches 0 run scoreboard players set @s ida.wind 60
$execute if score @s ida.skill matches 0 run function dungeons_arise:boss/spell/$(primary)/warn with entity @s data
$execute if score @s ida.skill matches 1 run function dungeons_arise:boss/spell/$(secondary)/warn with entity @s data
