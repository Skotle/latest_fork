tag @e[tag=fw.wall_emitter] remove fw.wall_live
scoreboard players add #wall_side fw.tmp 1
execute if score #wall_side fw.tmp matches 2.. run scoreboard players set #wall_side fw.tmp 0
execute if score #wall_side fw.tmp matches 0 run tag @e[tag=fw.wall_one,y_rotation=0..0] add fw.wall_live
execute if score #wall_side fw.tmp matches 0 run tag @e[tag=fw.wall_one,y_rotation=180..180] add fw.wall_live
execute if score #wall_side fw.tmp matches 1 run tag @e[tag=fw.wall_one,y_rotation=90..90] add fw.wall_live
execute if score #wall_side fw.tmp matches 1 run tag @e[tag=fw.wall_one,y_rotation=-90..-90] add fw.wall_live
