execute if score #skill db.skill matches 5..6 as @e[tag=db.boss,limit=1] at @e[tag=db.jump_origin,limit=1] run tp @s ~ ~ ~
scoreboard players set #pending db.tmp 0
kill @e[tag=db.core]
kill @e[tag=db.core_visual]
scoreboard players set #cast db.cast 0
scoreboard players set #safe db.safe 40
scoreboard players set #next db.next 4
execute as @a[scores={db.debt=1}] at @s run function desert_ball:theft/return
tellraw @a[tag=db.member] {"text": "공을 맞혔다! 2초 기절 — 도난품 반환!", "color": "gold"}
