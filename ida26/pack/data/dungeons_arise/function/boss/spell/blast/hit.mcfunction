$execute at @e[tag=ida.target,scores={ida.sid=$(id)},limit=1] run particle minecraft:explosion ~ ~0.5 ~ 1.5 0.8 1.5 0.05 55 force
$execute at @e[tag=ida.target,scores={ida.sid=$(id)},limit=1] as @a[predicate=dungeons_arise:boss/eligible,distance=..3] at @e[type=minecraft:marker,tag=ida.site,scores={ida.sid=$(id)},limit=1] if entity @s[distance=..24] run damage @s 5 minecraft:explosion by @e[tag=ida.boss,scores={ida.sid=$(id)},limit=1]
$execute at @e[tag=ida.target,scores={ida.sid=$(id)},limit=1] as @a[predicate=dungeons_arise:boss/eligible,distance=..3] at @e[type=minecraft:marker,tag=ida.site,scores={ida.sid=$(id)},limit=1] if entity @s[distance=..24] run effect give @s minecraft:slowness 2 0 true
playsound minecraft:entity.lightning_bolt.impact hostile @a[distance=..48] ~ ~ ~ 0.6 1
