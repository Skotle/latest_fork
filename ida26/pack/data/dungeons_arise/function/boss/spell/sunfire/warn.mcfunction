function dungeons_arise:boss/core/target with entity @s data
tellraw @a[predicate=dungeons_arise:boss/eligible,distance=..32] {"text":"⚠ 태양의 낙인 — 표식에서 벗어나세요!","color":"yellow"}
playsound minecraft:block.note_block.bell hostile @a[distance=..32] ~ ~ ~ 0.6 0.8
execute as @e[tag=ida.newtarget] store result score @s ida.sid run data get entity @s data.id 1
tag @e[tag=ida.newtarget] remove ida.newtarget
function dungeons_arise:boss/spell/sunfire/telegraph with entity @s data
