$execute as @e[tag=ida.boss,scores={ida.sid=$(id)}] run data modify entity @s DeathLootTable set value "minecraft:empty"
$kill @e[tag=ida.boss,scores={ida.sid=$(id)}]
function dungeons_arise:boss/site/cleanup with entity @s data
scoreboard players set @s ida.stage 0
scoreboard players set @s ida.idle 0
