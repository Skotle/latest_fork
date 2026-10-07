tag @a remove ida.spell_hit
$execute at @e[tag=ida.target,scores={ida.sid=$(id)}] as @a[predicate=dungeons_arise:boss/eligible,distance=..3] at @e[type=minecraft:marker,tag=ida.site,scores={ida.sid=$(id)},limit=1] if entity @s[distance=..24] run tag @s add ida.spell_hit
$execute at @e[tag=ida.target,scores={ida.sid=$(id)}] run particle minecraft:smoke ~ ~0.5 ~ 1.5 0.8 1.5 0.05 25 force
function dungeons_arise:boss/core/adds with entity @s data
tag @a remove ida.spell_hit
