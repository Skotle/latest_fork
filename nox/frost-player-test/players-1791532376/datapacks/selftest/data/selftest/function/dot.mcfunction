execute store result score #px fw.tmp run data get entity @s Pos[0] 1000
execute store result score #pz fw.tmp run data get entity @s Pos[2] 1000
scoreboard players operation #dx fw.tmp = #bx fw.tmp
scoreboard players operation #dz fw.tmp = #bz fw.tmp
scoreboard players operation #dx fw.tmp -= #px fw.tmp
scoreboard players operation #dz fw.tmp -= #pz fw.tmp
execute store result score #vx fw.tmp run data get entity @s Motion[0] 100
execute store result score #vz fw.tmp run data get entity @s Motion[2] 100
scoreboard players operation #dx fw.tmp *= #vx fw.tmp
scoreboard players operation #dz fw.tmp *= #vz fw.tmp
scoreboard players operation #dx fw.tmp += #dz fw.tmp
execute if score #dx fw.tmp matches 1.. run scoreboard players add #converging fw.tmp 1
