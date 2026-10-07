tag @a remove ida.spell_hit
$execute at @e[tag=ida.target,scores={ida.sid=$(id)}] as @a[predicate=dungeons_arise:boss/eligible,distance=..1.7] at @e[type=minecraft:marker,tag=ida.site,scores={ida.sid=$(id)},limit=1] if entity @s[distance=..24] run tag @s add ida.spell_hit
$execute at @e[tag=ida.target,scores={ida.sid=$(id)}] run particle minecraft:spore_blossom_air ~ ~0.5 ~ 0.85 0.8 0.85 0.05 25 force
$execute as @a[tag=ida.spell_hit] run damage @s 2 minecraft:magic by @e[tag=ida.boss,scores={ida.sid=$(id)},limit=1]
effect give @a[tag=ida.spell_hit] minecraft:poison 2 0 true
tag @a remove ida.spell_hit
