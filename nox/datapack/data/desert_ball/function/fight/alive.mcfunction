scoreboard players set #moving db.anim 0
scoreboard players add #time db.time 1
execute store result score #hp db.hp run data get entity @e[tag=db.boss,limit=1] Health 100
execute store result bossbar desert_ball:health value run data get entity @e[tag=db.boss,limit=1] Health
execute store result bossbar desert_ball:health max run scoreboard players get #max db.max
execute if score #safe db.safe matches 1.. run scoreboard players remove #safe db.safe 1
execute if score #pending db.tmp matches 1 run function desert_ball:skills/core_tick
execute if score #cast db.cast matches 1.. run function desert_ball:skills/casting
execute if score #cast db.cast matches 0 if score #safe db.safe matches 0 run scoreboard players remove #next db.next 1
execute if score #cast db.cast matches 0 if score #safe db.safe matches 0 if score #next db.next matches ..0 if entity @a[tag=db.active] run function desert_ball:skills/begin
execute if score #time db.time matches 37.. if score #safe db.safe matches 0 if score #skill db.skill matches 1..4 if entity @a[tag=db.active] as @e[tag=db.boss,limit=1] at @s run function desert_ball:fight/move
execute as @e[tag=db.shot] at @s run function desert_ball:shot/tick
execute as @e[tag=db.fall] at @s run function desert_ball:shot/fall_tick
function desert_ball:visual/tick
