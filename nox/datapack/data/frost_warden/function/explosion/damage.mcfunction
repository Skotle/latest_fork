execute store success score #hurt fw.tmp run damage @s 7 frost_warden:burst by @e[tag=fw.boss,limit=1]
execute if score #hurt fw.tmp matches 1 run scoreboard players add @s fw.hits 1
