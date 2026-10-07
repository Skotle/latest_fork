execute store result score @s nx.dx run data get entity @s Pos[0] 100
execute store result score @s nx.dz run data get entity @s Pos[2] 100
scoreboard players operation @s nx.dx -= #x nx.tmp
scoreboard players operation @s nx.dz -= #z nx.tmp
scoreboard players set #cos nx.tmp 707
scoreboard players set #sin nx.tmp -707
scoreboard players set #thousand nx.tmp 1000
scoreboard players set #tan nx.tmp 414
scoreboard players set #negative nx.tmp -1
scoreboard players operation @s nx.forward = @s nx.dx
scoreboard players operation @s nx.forward *= #cos nx.tmp
scoreboard players operation @s nx.side = @s nx.dz
scoreboard players operation @s nx.side *= #sin nx.tmp
scoreboard players operation @s nx.forward += @s nx.side
scoreboard players operation @s nx.forward /= #thousand nx.tmp
scoreboard players operation @s nx.side = @s nx.dz
scoreboard players operation @s nx.side *= #cos nx.tmp
scoreboard players operation @s nx.tmp = @s nx.dx
scoreboard players operation @s nx.tmp *= #sin nx.tmp
scoreboard players operation @s nx.side -= @s nx.tmp
scoreboard players operation @s nx.side /= #thousand nx.tmp
execute if score @s nx.side matches ..-1 run scoreboard players operation @s nx.side *= #negative nx.tmp
scoreboard players operation @s nx.side *= #thousand nx.tmp
scoreboard players operation @s nx.forward *= #tan nx.tmp
execute if score @s nx.forward matches 0.. if score @s nx.side <= @s nx.forward run tag @s add nox.shelter
