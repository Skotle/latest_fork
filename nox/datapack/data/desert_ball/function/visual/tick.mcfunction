execute as @e[tag=db.body] at @e[tag=db.boss,limit=1] run tp @s ~ ~ ~ ~ 0
execute if score #skill db.skill matches 2 run item replace entity @e[tag=db.part.torso,limit=1] contents with minecraft:paper[minecraft:item_model="desert_ball:bare"]
execute unless score #skill db.skill matches 2 run item replace entity @e[tag=db.part.torso,limit=1] contents with minecraft:paper[minecraft:item_model="desert_ball:torso"]
scoreboard players operation #frame db.motion = #time db.time
scoreboard players set #sixteen db.tmp 16
scoreboard players operation #frame db.motion %= #sixteen db.tmp
execute if score #skill db.skill matches 5..6 if score #cast db.cast matches 1.. run function desert_ball:visual/jump_frame
execute if score #frame db.motion matches 0 run function desert_ball:visual/pose/0
execute if score #frame db.motion matches 1 run function desert_ball:visual/pose/1
execute if score #frame db.motion matches 2 run function desert_ball:visual/pose/2
execute if score #frame db.motion matches 3 run function desert_ball:visual/pose/3
execute if score #frame db.motion matches 4 run function desert_ball:visual/pose/4
execute if score #frame db.motion matches 5 run function desert_ball:visual/pose/5
execute if score #frame db.motion matches 6 run function desert_ball:visual/pose/6
execute if score #frame db.motion matches 7 run function desert_ball:visual/pose/7
execute if score #frame db.motion matches 8 run function desert_ball:visual/pose/8
execute if score #frame db.motion matches 9 run function desert_ball:visual/pose/9
execute if score #frame db.motion matches 10 run function desert_ball:visual/pose/10
execute if score #frame db.motion matches 11 run function desert_ball:visual/pose/11
execute if score #frame db.motion matches 12 run function desert_ball:visual/pose/12
execute if score #frame db.motion matches 13 run function desert_ball:visual/pose/13
execute if score #frame db.motion matches 14 run function desert_ball:visual/pose/14
execute if score #frame db.motion matches 15 run function desert_ball:visual/pose/15
