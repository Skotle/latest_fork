tag @a remove ida.spell_hit
$execute at @e[tag=ida.target,scores={ida.sid=$(id)}] as @a[predicate=dungeons_arise:boss/eligible,distance=..1.2] at @e[type=minecraft:marker,tag=ida.site,scores={ida.sid=$(id)},limit=1] if entity @s[distance=..24] run tag @s add ida.spell_hit
$execute at @e[tag=ida.target,scores={ida.sid=$(id)}] run particle minecraft:soul ~ ~0.5 ~ 0.6 0.8 0.6 0.05 25 force
$execute at @e[tag=ida.target,scores={ida.sid=$(id)}] run summon minecraft:evoker_fangs ~ ~ ~ {Tags:["ida.newfang"]}
$execute as @e[tag=ida.newfang] run data modify entity @s Owner set from entity @e[tag=ida.boss,scores={ida.sid=$(id)},limit=1] UUID
tag @e[tag=ida.newfang] remove ida.newfang
tag @a remove ida.spell_hit
