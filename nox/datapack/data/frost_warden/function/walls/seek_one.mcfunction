execute if block ~ ~ ~ #frost_warden:blast_pass run return run function frost_warden:walls/place_one
scoreboard players add #wall_steps fw.tmp 1
execute if score #wall_steps fw.tmp matches ..20 positioned ^ ^ ^.5 run function frost_warden:walls/seek_one
