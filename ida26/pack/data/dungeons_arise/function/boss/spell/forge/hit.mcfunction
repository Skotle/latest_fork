tag @a remove ida.spell_hit
$execute at @e[tag=ida.target,scores={ida.sid=$(id)}] as @a[predicate=dungeons_arise:boss/eligible,distance=..1.3] at @e[type=minecraft:marker,tag=ida.site,scores={ida.sid=$(id)},limit=1] if entity @s[distance=..24] run tag @s add ida.spell_hit
$execute at @e[tag=ida.target,scores={ida.sid=$(id)}] run particle minecraft:flame ~ ~0.5 ~ 0.65 0.8 0.65 0.05 25 force
$execute as @a[tag=ida.spell_hit] run damage @s 4 minecraft:on_fire by @e[tag=ida.boss,scores={ida.sid=$(id)},limit=1]
effect give @a[tag=ida.spell_hit] minecraft:weakness 2 0 true
execute if score @s ida.phase matches 2 run function dungeons_arise:boss/core/adds with entity @s data
playsound minecraft:entity.lightning_bolt.impact hostile @a[distance=..48] ~ ~ ~ 0.6 1
tag @a remove ida.spell_hit
