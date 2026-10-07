function dungeons_arise:boss/core/target with entity @s data
tellraw @a[predicate=dungeons_arise:boss/eligible,distance=..32] {"text":"⚠ 발파 충격파 — 여러 표식을 피해 이동하세요!","color":"yellow"}
playsound minecraft:block.note_block.bell hostile @a[distance=..32] ~ ~ ~ 0.6 0.8
$execute if entity @e[tag=ida.aim,scores={ida.sid=$(id)},limit=1] at @e[tag=ida.aim,scores={ida.sid=$(id)},limit=1] positioned ~-3 ~0 ~0 run summon minecraft:marker ~ ~ ~ {Tags:["ida.target","ida.newtarget"],data:{id:$(id)}}
$execute if entity @e[tag=ida.aim,scores={ida.sid=$(id)},limit=1] at @e[tag=ida.aim,scores={ida.sid=$(id)},limit=1] positioned ~3 ~0 ~0 run summon minecraft:marker ~ ~ ~ {Tags:["ida.target","ida.newtarget"],data:{id:$(id)}}
$execute if entity @e[tag=ida.aim,scores={ida.sid=$(id)},limit=1] at @e[tag=ida.aim,scores={ida.sid=$(id)},limit=1] positioned ~0 ~0 ~3 run summon minecraft:marker ~ ~ ~ {Tags:["ida.target","ida.newtarget"],data:{id:$(id)}}
execute as @e[tag=ida.newtarget] store result score @s ida.sid run data get entity @s data.id 1
tag @e[tag=ida.newtarget] remove ida.newtarget
function dungeons_arise:boss/spell/blast/telegraph with entity @s data
