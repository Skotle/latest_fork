tag @a remove ida.spell_hit
$execute at @e[tag=ida.target,scores={ida.sid=$(id)}] as @a[predicate=dungeons_arise:boss/eligible,distance=..1.8] at @e[type=minecraft:marker,tag=ida.site,scores={ida.sid=$(id)},limit=1] if entity @s[distance=..24] run tag @s add ida.spell_hit
$execute at @e[tag=ida.target,scores={ida.sid=$(id)}] run particle minecraft:crit ~ ~0.5 ~ 0.9 0.8 0.9 0.05 25 force
$execute as @a[tag=ida.spell_hit] run damage @s 5 minecraft:mob_attack by @e[tag=ida.boss,scores={ida.sid=$(id)},limit=1]
effect give @a[tag=ida.spell_hit] minecraft:weakness 2 0 true
tag @a remove ida.spell_hit
