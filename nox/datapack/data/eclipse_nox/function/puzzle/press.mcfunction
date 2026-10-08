scoreboard players set #bell nx.tmp 0
execute if entity @s[tag=nox.bell1] run scoreboard players set #bell nx.tmp 1
execute if entity @s[tag=nox.bell2] run scoreboard players set #bell nx.tmp 2
execute if entity @s[tag=nox.bell3] run scoreboard players set #bell nx.tmp 3
scoreboard players set #lock nx.lock 20
execute at @s run playsound eclipse_nox:bell_low master @a[tag=nox.member] ~ ~ ~ 1 1
scoreboard players set #expected nx.tmp 1
execute if score #step nx.step matches 1 run scoreboard players set #expected nx.tmp 3
execute if score #step nx.step matches 2 run scoreboard players set #expected nx.tmp 2
execute if score #bell nx.tmp = #last nx.last at @s run function eclipse_nox:puzzle/overload
execute if score #bell nx.tmp = #expected nx.tmp run scoreboard players add #step nx.step 1
execute unless score #bell nx.tmp = #expected nx.tmp run scoreboard players set #step nx.step 0
execute unless score #bell nx.tmp = #expected nx.tmp run tellraw @a[tag=nox.member] {"text": "음이 어긋났다. 봉인종 순서를 처음부터 다시 맞춰라.", "color": "gold"}
scoreboard players operation #last nx.last = #bell nx.tmp
execute unless score #bell nx.tmp = #expected nx.tmp run scoreboard players add #mistakes nx.tmp 1
