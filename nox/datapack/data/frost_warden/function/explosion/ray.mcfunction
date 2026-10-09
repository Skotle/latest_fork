execute unless block ~ ~ ~ #frost_warden:blast_pass run return 0
execute if entity @e[tag=fw.ray_target,distance=..0.25] run return run function frost_warden:explosion/damage
scoreboard players add #ray fw.tmp 1
execute if score #ray fw.tmp matches ..24 positioned ^ ^ ^.2 run function frost_warden:explosion/ray
