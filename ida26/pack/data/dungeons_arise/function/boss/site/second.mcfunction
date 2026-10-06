execute if score #difficulty ida.tmp matches 0 if score @s ida.stage matches 1 run function dungeons_arise:boss/site/abort with entity @s data
$execute unless entity @s[tag=ida.manualsite] if score #enabled ida.cfg matches 1 if score #difficulty ida.tmp matches 1.. if score @s ida.stage matches 0 if entity @a[predicate=dungeons_arise:boss/eligible,distance=..96] run function dungeons_arise:boss/$(kind)/start
execute if score @s ida.stage matches 1 run function dungeons_arise:boss/site/active with entity @s data
execute if score @s ida.stage matches 2 run scoreboard players add @s ida.cool 1
execute if score @s ida.stage matches 2 if score @s ida.cool >= #respawn ida.cfg run scoreboard players set @s ida.stage 0
