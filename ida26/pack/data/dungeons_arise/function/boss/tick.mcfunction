scoreboard players add #clock ida.tick 1
function dungeons_arise:boss/contain
execute if score #clock ida.tick matches 5.. run function dungeons_arise:boss/fast
execute if score #clock ida.tick matches 20.. run function dungeons_arise:boss/second
execute if score #clock ida.tick matches 20.. run scoreboard players set #clock ida.tick 0
