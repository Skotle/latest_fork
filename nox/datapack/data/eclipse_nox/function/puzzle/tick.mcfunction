scoreboard players add #puzzletime nx.tmp 1
execute as @e[tag=nox.bell,type=minecraft:interaction] if data entity @s interaction run function eclipse_nox:puzzle/interact
execute if score #puzzletime nx.tmp matches 24.. run function eclipse_nox:puzzle/pulse
execute if score #step nx.step matches 3 run function eclipse_nox:puzzle/success
