function dungeons_arise:boss/site/boundary
$bossbar set dungeons_arise:encounter_$(id) players @a[predicate=dungeons_arise:boss/eligible,distance=..96]
$execute as @e[tag=ida.boss,scores={ida.sid=$(id)},limit=1] store result score @s ida.hp run data get entity @s Health 100
$execute as @e[tag=ida.boss,scores={ida.sid=$(id)},limit=1] store result bossbar dungeons_arise:encounter_$(id) value run data get entity @s Health 1
execute unless entity @a[predicate=dungeons_arise:boss/eligible,distance=..128] run scoreboard players add @s ida.idle 1
execute if entity @a[predicate=dungeons_arise:boss/eligible,distance=..128] run scoreboard players set @s ida.idle 0
$execute unless entity @e[tag=ida.boss,scores={ida.sid=$(id),ida.hp=1..},limit=1] run function dungeons_arise:boss/site/victory with entity @s data
execute if score @s ida.stage matches 1 if score @s ida.idle >= #abandon ida.cfg run function dungeons_arise:boss/site/abort with entity @s data
