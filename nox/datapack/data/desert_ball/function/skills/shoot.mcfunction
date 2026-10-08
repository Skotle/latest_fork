execute as @e[tag=db.boss,limit=1] at @s facing entity @a[tag=db.active,sort=nearest,limit=1] eyes run tp @s ~ ~ ~ ~ 0
execute at @e[tag=db.boss,limit=1] rotated as @e[tag=db.boss,limit=1] positioned ~ ~1.1 ~ run summon minecraft:marker ~ ~ ~ {Tags:["db.owned","db.shot","db.newshot"]}
execute if score #skill db.skill matches 5 as @e[tag=db.newshot] at @e[tag=db.boss,limit=1] run tp @s ~ ~2.45 ~
execute if score #skill db.skill matches 6 as @e[tag=db.newshot] at @e[tag=db.boss,limit=1] run tp @s ~ ~1.9 ~
execute as @e[tag=db.newshot] rotated as @e[tag=db.boss,limit=1] run tp @s ~ ~ ~ ~ 0
scoreboard players set @e[tag=db.newshot] db.time 45
scoreboard players operation @e[tag=db.newshot] db.skill = #skill db.skill
execute at @e[tag=db.newshot,limit=1] run summon minecraft:item_display ~ ~ ~ {"Tags":["db.owned","db.visual","db.shot_visual","db.newvisual"],"Invulnerable":true,"width":0.0,"height":0.0,"item":{"id":"minecraft:paper","count":1,"components":{"minecraft:item_model":"desert_ball:ball"}},"item_display":"fixed","teleport_duration":1,"interpolation_duration":2,"transformation":{"translation":[0,0,0],"scale":[1.15,1.15,1.15],"left_rotation":[0,0,0,1],"right_rotation":[0,0,0,1]}}
scoreboard players add #ball db.owner 1
scoreboard players operation @e[tag=db.newshot] db.owner = #ball db.owner
scoreboard players operation @e[tag=db.newvisual] db.owner = #ball db.owner
execute as @e[tag=db.newshot] at @s facing entity @a[tag=db.active,sort=nearest,limit=1] eyes run tp @s ~ ~ ~ ~ ~
tag @e[tag=db.newshot] remove db.newshot
tag @e[tag=db.newvisual] remove db.newvisual
