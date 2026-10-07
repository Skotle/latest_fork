$scoreboard players set @s ida.sid $(id)
$scoreboard players set @s ida.max $(hp)
scoreboard players operation @s ida.max *= #hundred ida.tmp
scoreboard players set @s ida.stage 0
scoreboard players set @s ida.phase 1
scoreboard players set @s ida.cd 0
scoreboard players set @s ida.wind 0
scoreboard players set @s ida.skill 0
scoreboard players set @s ida.age 0
$team add ida$(id)
$team modify ida$(id) friendlyFire false
$team modify ida$(id) collisionRule pushOtherTeams
$team join ida$(id) @s
effect give @s minecraft:fire_resistance infinite 0 true
tag @s remove ida.newboss
function dungeons_arise:boss/visual/setup with entity @s data
