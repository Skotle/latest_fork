$execute at @e[type=minecraft:marker,tag=ida.site,scores={ida.sid=$(id)},limit=1] unless entity @a[predicate=dungeons_arise:boss/eligible,distance=..24] run return 0
execute if score @s ida.stage matches 1..2 run return 0
scoreboard players add @s ida.cd 1
$scoreboard players set #period ida.tmp $(period)
execute if score @s ida.phase matches 2 run scoreboard players remove #period ida.tmp 1
execute if score @s ida.cd >= #period ida.tmp run function dungeons_arise:boss/core/begin with entity @s data
