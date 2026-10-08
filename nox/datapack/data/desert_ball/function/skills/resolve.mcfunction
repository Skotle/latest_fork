execute if score #skill db.skill matches 5..6 as @e[tag=db.boss,limit=1] at @e[tag=db.jump_origin,limit=1] run tp @s ~ ~ ~
scoreboard players set #pending db.tmp 0
kill @e[tag=db.core]
kill @e[tag=db.core_visual]
scoreboard players set #safe db.safe 10
execute if score #skill db.skill matches 2 run function desert_ball:skills/ambush
execute if score #skill db.skill matches 4 run function desert_ball:skills/shoot
