$kill @e[tag=ida.target,scores={ida.sid=$(id)}]
$execute at @e[type=minecraft:marker,tag=ida.site,scores={ida.sid=$(id)},limit=1] at @a[predicate=dungeons_arise:boss/eligible,distance=..24,sort=nearest,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["ida.target","ida.newtarget"],data:{id:$(id)}}
execute as @e[tag=ida.newtarget] store result score @s ida.sid run data get entity @s data.id 1
tag @e[tag=ida.newtarget] remove ida.newtarget
