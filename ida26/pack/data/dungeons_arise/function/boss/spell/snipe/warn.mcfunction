function dungeons_arise:boss/core/target with entity @s data
tellraw @a[predicate=dungeons_arise:boss/eligible,distance=..32] {"text":"⚠ 조준 사격 — 직선 공격! 옆으로 피하세요!","color":"yellow"}
playsound minecraft:block.note_block.bell hostile @a[distance=..32] ~ ~ ~ 0.6 0.8
$execute if entity @e[tag=ida.aim,scores={ida.sid=$(id)},limit=1] facing entity @e[tag=ida.aim,scores={ida.sid=$(id)},limit=1] feet run tp @s ~ ~ ~ ~ 0
$execute if entity @e[tag=ida.aim,scores={ida.sid=$(id)},limit=1] positioned ^0 ^0 ^2 run summon minecraft:marker ~ ~ ~ {Tags:["ida.target","ida.newtarget"],data:{id:$(id)}}
$execute if entity @e[tag=ida.aim,scores={ida.sid=$(id)},limit=1] positioned ^0 ^0 ^4 run summon minecraft:marker ~ ~ ~ {Tags:["ida.target","ida.newtarget"],data:{id:$(id)}}
$execute if entity @e[tag=ida.aim,scores={ida.sid=$(id)},limit=1] positioned ^0 ^0 ^6 run summon minecraft:marker ~ ~ ~ {Tags:["ida.target","ida.newtarget"],data:{id:$(id)}}
$execute if entity @e[tag=ida.aim,scores={ida.sid=$(id)},limit=1] positioned ^0 ^0 ^8 run summon minecraft:marker ~ ~ ~ {Tags:["ida.target","ida.newtarget"],data:{id:$(id)}}
$execute if entity @e[tag=ida.aim,scores={ida.sid=$(id)},limit=1] positioned ^0 ^0 ^10 run summon minecraft:marker ~ ~ ~ {Tags:["ida.target","ida.newtarget"],data:{id:$(id)}}
$execute if entity @e[tag=ida.aim,scores={ida.sid=$(id)},limit=1] positioned ^0 ^0 ^12 run summon minecraft:marker ~ ~ ~ {Tags:["ida.target","ida.newtarget"],data:{id:$(id)}}
$kill @e[tag=ida.aim,scores={ida.sid=$(id)}]
execute as @e[tag=ida.newtarget] store result score @s ida.sid run data get entity @s data.id 1
tag @e[tag=ida.newtarget] remove ida.newtarget
function dungeons_arise:boss/spell/snipe/telegraph with entity @s data
