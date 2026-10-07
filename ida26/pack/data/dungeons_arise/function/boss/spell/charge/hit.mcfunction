tag @a remove ida.spell_hit
$execute at @e[tag=ida.target,scores={ida.sid=$(id)}] as @a[predicate=dungeons_arise:boss/eligible,distance=..1.2] at @e[type=minecraft:marker,tag=ida.site,scores={ida.sid=$(id)},limit=1] if entity @s[distance=..24] run tag @s add ida.spell_hit
$execute at @e[tag=ida.target,scores={ida.sid=$(id)}] run particle minecraft:cloud ~ ~0.5 ~ 0.6 0.8 0.6 0.05 25 force
$execute as @a[tag=ida.spell_hit] run damage @s 4 minecraft:mob_attack by @e[tag=ida.boss,scores={ida.sid=$(id)},limit=1]
effect give @a[tag=ida.spell_hit] minecraft:slowness 2 1 true
tag @a remove ida.spell_hit
