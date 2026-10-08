tellraw @a[tag=db.member] {"text": "오버헤드킥! 표시된 착탄점 밖으로 이동하거나 준비 공을 사격하세요.", "color": "gold"}
execute as @a[tag=db.active] at @s run summon minecraft:marker ~ ~ ~ {Tags:["db.owned","db.fall","db.newfall"]}
scoreboard players set @e[tag=db.newfall] db.time 20
tag @e[tag=db.newfall] remove db.newfall
execute at @e[tag=db.boss,limit=1] run function desert_ball:skills/shoot
