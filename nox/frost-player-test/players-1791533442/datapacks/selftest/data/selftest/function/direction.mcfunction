execute store result score #vx fw.tmp run data get entity @s Motion[0] 1000
execute store result score #vz fw.tmp run data get entity @s Motion[2] 1000
execute if score #vx fw.tmp matches 2000.. run scoreboard players add #east fw.tmp 1
execute if score #vx fw.tmp matches ..-2000 run scoreboard players add #west fw.tmp 1
execute if score #vz fw.tmp matches 2000.. run scoreboard players add #north fw.tmp 1
execute if score #vz fw.tmp matches ..-2000 run scoreboard players add #south fw.tmp 1
