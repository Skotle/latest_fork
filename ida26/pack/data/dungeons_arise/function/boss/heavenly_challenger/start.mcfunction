scoreboard players set #players ida.tmp 0
execute as @a[predicate=dungeons_arise:boss/eligible,distance=..96] run scoreboard players add #players ida.tmp 1
execute if score #players ida.tmp matches ..0 run scoreboard players set #players ida.tmp 1
execute if score #players ida.tmp matches 5.. run scoreboard players set #players ida.tmp 4
scoreboard players remove #players ida.tmp 1
scoreboard players operation #players ida.tmp *= #quarter ida.tmp
scoreboard players add #players ida.tmp 100
scoreboard players set #hp ida.tmp 280
scoreboard players operation #hp ida.tmp *= #players ida.tmp
scoreboard players operation #hp ida.tmp /= #hundred ida.tmp
execute store result entity @s data.hp int 1 run scoreboard players get #hp ida.tmp
scoreboard players set #spawned ida.tmp 0
execute unless data entity @s data.anchored at @a[predicate=dungeons_arise:boss/eligible,distance=..96,sort=nearest,limit=1] run function dungeons_arise:boss/heavenly_challenger/search
execute if data entity @s data.anchored if score #spawned ida.tmp matches 0 run function dungeons_arise:boss/heavenly_challenger/search
execute if score #spawned ida.tmp matches 1 run function dungeons_arise:boss/site/restore with entity @s data
