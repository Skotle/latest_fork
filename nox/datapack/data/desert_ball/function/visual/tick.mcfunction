scoreboard players set #mode db.anim 0
execute if score #moving db.anim matches 1 run scoreboard players set #mode db.anim 1
execute if score #safe db.safe matches 1..10 run scoreboard players set #mode db.anim 10
execute if score #safe db.safe matches 11.. run scoreboard players set #mode db.anim 8
scoreboard players operation #frame db.motion = #time db.time
scoreboard players set #frames db.tmp 24
scoreboard players operation #frame db.motion %= #frames db.tmp
execute if score #cast db.cast matches 1.. if score #skill db.skill matches 1 run scoreboard players set #mode db.anim 2
execute if score #cast db.cast matches 1.. if score #skill db.skill matches 2 run scoreboard players set #mode db.anim 3
execute if score #cast db.cast matches 1.. if score #skill db.skill matches 3 run scoreboard players set #mode db.anim 4
execute if score #cast db.cast matches 1.. if score #skill db.skill matches 4 run scoreboard players set #mode db.anim 5
execute if score #cast db.cast matches 1.. if score #skill db.skill matches 5 run scoreboard players set #mode db.anim 6
execute if score #cast db.cast matches 1.. if score #skill db.skill matches 6 run scoreboard players set #mode db.anim 7
execute if score #cast db.cast matches 1.. run function desert_ball:visual/cast_frame
execute if score #cast db.cast matches 0 if score #safe db.safe matches 1..10 run function desert_ball:visual/recover_frame
execute if score #follow db.anim matches 1.. if score #skill db.skill matches 2 if score #cast db.cast matches 0 if score #safe db.safe matches ..10 run function desert_ball:visual/ambush_frame
execute if score #follow db.anim matches 1.. run scoreboard players remove #follow db.anim 1
execute if score #time db.time matches ..36 if score #cast db.cast matches 0 if score #safe db.safe matches 0 run function desert_ball:visual/intro_frame
execute as @e[tag=db.body] at @e[tag=db.boss,limit=1] run tp @s ~ ~ ~ ~ 0
execute if score #skill db.skill matches 2 run item replace entity @e[tag=db.part.torso,limit=1] contents with minecraft:paper[minecraft:item_model="desert_ball:bare"]
execute unless score #skill db.skill matches 2 run item replace entity @e[tag=db.part.torso,limit=1] contents with minecraft:paper[minecraft:item_model="desert_ball:torso"]
execute if score #skill db.skill matches 2 run item replace entity @e[tag=db.part.left_arm,limit=1] contents with minecraft:paper[minecraft:item_model="desert_ball:left_arm_bare"]
execute unless score #skill db.skill matches 2 run item replace entity @e[tag=db.part.left_arm,limit=1] contents with minecraft:paper[minecraft:item_model="desert_ball:left_arm"]
execute if score #skill db.skill matches 2 run item replace entity @e[tag=db.part.right_arm,limit=1] contents with minecraft:paper[minecraft:item_model="desert_ball:right_arm_bare"]
execute unless score #skill db.skill matches 2 run item replace entity @e[tag=db.part.right_arm,limit=1] contents with minecraft:paper[minecraft:item_model="desert_ball:right_arm"]
execute if score #mode db.anim matches 0 run function desert_ball:visual/idle/dispatch
execute if score #mode db.anim matches 1 run function desert_ball:visual/run/dispatch
execute if score #mode db.anim matches 2 run function desert_ball:visual/shoot/dispatch
execute if score #mode db.anim matches 3 run function desert_ball:visual/ninja/dispatch
execute if score #mode db.anim matches 4 run function desert_ball:visual/noshow/dispatch
execute if score #mode db.anim matches 5 run function desert_ball:visual/crab/dispatch
execute if score #mode db.anim matches 6 run function desert_ball:visual/header/dispatch
execute if score #mode db.anim matches 7 run function desert_ball:visual/overhead/dispatch
execute if score #mode db.anim matches 8 run function desert_ball:visual/stagger/dispatch
execute if score #mode db.anim matches 9 run function desert_ball:visual/celebrate/dispatch
execute if score #mode db.anim matches 10 run function desert_ball:visual/recover/dispatch
