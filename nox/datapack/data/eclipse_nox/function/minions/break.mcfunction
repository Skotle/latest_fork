scoreboard players set #break nx.add 0
scoreboard players set #safe nx.safe 40
scoreboard players set #next nx.next 0
scoreboard players set #expose nx.expose 1
scoreboard players set #counter nx.move 1
execute store result score #oldhp nx.hp run data get entity @e[tag=nox.boss,limit=1] Health 100
tellraw @a[tag=nox.member] {"text":"파수꾼의 반격: 녹스에게 주는 피해 2배, 2초!","color":"gold"}
