scoreboard players set #pending db.tmp 0
scoreboard players set #skill db.skill 1
scoreboard players set #state db.state 1
scoreboard players set #time db.time 0
scoreboard players set #cycle db.cycle 0
scoreboard players set #idle db.idle 0
scoreboard players set #safe db.safe 0
scoreboard players set #cast db.cast 0
scoreboard players set #next db.next 40
scoreboard players set #max db.max 500
execute as @a[tag=db.member] run scoreboard players add #max db.max 250
execute if score #max db.max matches 1251.. run scoreboard players set #max db.max 1250
execute as @a[tag=db.member] run scoreboard players add @s nx.death 0
execute as @a[tag=db.member] run scoreboard players add @s nx.leave 0
execute as @a[tag=db.member] run scoreboard players operation @s db.olddeath = @s nx.death
execute as @a[tag=db.member] run scoreboard players operation @s db.oldleave = @s nx.leave
execute store result storage desert_ball:runtime hp int 1 run scoreboard players get #max db.max
function desert_ball:fight/carrier with storage desert_ball:runtime
summon minecraft:item_display ~ ~ ~ {"Tags":["db.owned","db.visual","db.body","db.part.torso"],"Invulnerable":true,"width":0.0,"height":0.0,"item":{"id":"minecraft:paper","count":1,"components":{"minecraft:item_model":"desert_ball:torso"}},"item_display":"fixed","teleport_duration":1,"interpolation_duration":2,"transformation":{"translation":[0,1.35,0],"scale":[1.15,1.15,1.15],"left_rotation":[0,0,0,1],"right_rotation":[0,0,0,1]}}
summon minecraft:item_display ~ ~ ~ {"Tags":["db.owned","db.visual","db.body","db.part.head"],"Invulnerable":true,"width":0.0,"height":0.0,"item":{"id":"minecraft:paper","count":1,"components":{"minecraft:item_model":"desert_ball:head"}},"item_display":"fixed","teleport_duration":1,"interpolation_duration":2,"transformation":{"translation":[0,2.13,0],"scale":[1.15,1.15,1.15],"left_rotation":[0,0,0,1],"right_rotation":[0,0,0,1]}}
summon minecraft:item_display ~ ~ ~ {"Tags":["db.owned","db.visual","db.body","db.part.left_arm"],"Invulnerable":true,"width":0.0,"height":0.0,"item":{"id":"minecraft:paper","count":1,"components":{"minecraft:item_model":"desert_ball:left_arm"}},"item_display":"fixed","teleport_duration":1,"interpolation_duration":2,"transformation":{"translation":[-0.49,1.55,0],"scale":[1.15,1.15,1.15],"left_rotation":[0,0,0,1],"right_rotation":[0,0,0,1]}}
summon minecraft:item_display ~ ~ ~ {"Tags":["db.owned","db.visual","db.body","db.part.right_arm"],"Invulnerable":true,"width":0.0,"height":0.0,"item":{"id":"minecraft:paper","count":1,"components":{"minecraft:item_model":"desert_ball:right_arm"}},"item_display":"fixed","teleport_duration":1,"interpolation_duration":2,"transformation":{"translation":[0.49,1.55,0],"scale":[1.15,1.15,1.15],"left_rotation":[0,0,0,1],"right_rotation":[0,0,0,1]}}
summon minecraft:item_display ~ ~ ~ {"Tags":["db.owned","db.visual","db.body","db.part.left_leg"],"Invulnerable":true,"width":0.0,"height":0.0,"item":{"id":"minecraft:paper","count":1,"components":{"minecraft:item_model":"desert_ball:left_leg"}},"item_display":"fixed","teleport_duration":1,"interpolation_duration":2,"transformation":{"translation":[-0.22,0.54,0],"scale":[1.15,1.15,1.15],"left_rotation":[0,0,0,1],"right_rotation":[0,0,0,1]}}
summon minecraft:item_display ~ ~ ~ {"Tags":["db.owned","db.visual","db.body","db.part.right_leg"],"Invulnerable":true,"width":0.0,"height":0.0,"item":{"id":"minecraft:paper","count":1,"components":{"minecraft:item_model":"desert_ball:right_leg"}},"item_display":"fixed","teleport_duration":1,"interpolation_duration":2,"transformation":{"translation":[0.22,0.54,0],"scale":[1.15,1.15,1.15],"left_rotation":[0,0,0,1],"right_rotation":[0,0,0,1]}}
summon minecraft:item_display ~ ~ ~ {"Tags":["db.owned","db.visual","db.body","db.carried_ball"],"Invulnerable":true,"width":0.0,"height":0.0,"item":{"id":"minecraft:paper","count":1,"components":{"minecraft:item_model":"desert_ball:ball"}},"item_display":"fixed","teleport_duration":1,"interpolation_duration":2,"transformation":{"translation":[0,0.45,0.65],"scale":[1.15,1.15,1.15],"left_rotation":[0,0,0,1],"right_rotation":[0,0,0,1]}}
bossbar set desert_ball:health players @a[tag=db.member]
bossbar set desert_ball:health visible true
tellraw @a[tag=db.member] {"text": "베르나베우의 사막 결전! 날강두·젖통닌자·노쇼·꽃게드리블·헤딩골·오버헤드킥", "color": "gold"}
