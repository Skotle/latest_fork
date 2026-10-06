scoreboard players operation #half ida.tmp = @s ida.max
scoreboard players operation #half ida.tmp /= #two ida.tmp
execute if score @s ida.phase matches 1 if score @s ida.hp <= #half ida.tmp run function dungeons_arise:boss/core/enrage with entity @s data
execute if score @s ida.wind matches 1.. run scoreboard players remove @s ida.wind 5
execute if score @s ida.wind matches 1.. run function dungeons_arise:boss/core/telegraph with entity @s data
execute if score @s ida.wind matches ..0 if score @s ida.stage matches 1 run function dungeons_arise:boss/core/resolve with entity @s data
execute if score #clock ida.tick matches 20 run function dungeons_arise:boss/core/second with entity @s data
