$execute at @e[tag=ida.target,scores={ida.sid=$(id)},limit=1] run particle minecraft:flame ~ ~0.5 ~ 1.25 0.8 1.25 0.05 55 force
$execute at @e[tag=ida.target,scores={ida.sid=$(id)},limit=1] as @a[predicate=dungeons_arise:boss/eligible,distance=..2.5] at @e[type=minecraft:marker,tag=ida.site,scores={ida.sid=$(id)},limit=1] if entity @s[distance=..24] run damage @s 4 minecraft:on_fire by @e[tag=ida.boss,scores={ida.sid=$(id)},limit=1]
playsound minecraft:entity.lightning_bolt.impact hostile @a[distance=..48] ~ ~ ~ 0.6 1
