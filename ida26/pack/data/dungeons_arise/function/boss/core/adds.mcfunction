scoreboard players set #adds ida.tmp 0
$execute as @e[tag=ida.add,scores={ida.sid=$(id)}] run scoreboard players add #adds ida.tmp 1
$execute if score #adds ida.tmp matches ..2 positioned ~2 ~ ~ run function dungeons_arise:boss/$(kind)/add with entity @s data
$execute if score #adds ida.tmp matches ..2 positioned ~-2 ~ ~ run function dungeons_arise:boss/$(kind)/add with entity @s data
