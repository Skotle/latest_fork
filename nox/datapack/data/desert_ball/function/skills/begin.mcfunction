kill @e[tag=db.core]
kill @e[tag=db.core_visual]
scoreboard players set #pending db.tmp 0
scoreboard players add #cycle db.cycle 1
execute if score #cycle db.cycle matches 7.. run scoreboard players set #cycle db.cycle 1
scoreboard players operation #skill db.skill = #cycle db.cycle
scoreboard players operation #ratio db.tmp = #hp db.hp
scoreboard players operation #ratio db.tmp /= #max db.max
execute if score #ratio db.tmp matches 66.. if score #skill db.skill matches 2 run scoreboard players set #skill db.skill 4
execute if score #ratio db.tmp matches 66.. if score #skill db.skill matches 3 run scoreboard players set #skill db.skill 5
execute if score #ratio db.tmp matches 31.. if score #skill db.skill matches 6 run scoreboard players set #skill db.skill 5
scoreboard players set #cast db.cast 24
scoreboard players set #next db.next 12
execute if score #skill db.skill matches 2 run scoreboard players set #cast db.cast 40
execute if score #skill db.skill matches 3 run scoreboard players set #cast db.cast 40
execute if score #skill db.skill matches 4 run scoreboard players set #cast db.cast 36
execute if score #skill db.skill matches 5..6 run scoreboard players set #cast db.cast 30
execute as @e[tag=db.boss,limit=1] at @s facing entity @a[tag=db.active,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
kill @e[tag=db.jump_origin]
execute at @e[tag=db.boss,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["db.owned","db.jump_origin"]}
execute if score #skill db.skill matches 1 run tellraw @a[tag=db.member] {"text": "날강두! 소지품을 노린다. 슈팅을 피하고 도주하는 몸통을 사격하세요.", "color": "gold"}
execute if score #skill db.skill matches 2 run tellraw @a[tag=db.member] {"text": "젖통닌자! 모래 연막 — 재등장 발자국과 가슴 표식을 사격하세요.", "color": "gold"}
execute if score #skill db.skill matches 3 run function desert_ball:skills/noshow
execute if score #skill db.skill matches 5 run tellraw @a[tag=db.member] {"text": "헤딩골! 떠오른 공을 맞히면 2초 기절합니다.", "color": "gold"}
execute if score #skill db.skill matches 6 run tellraw @a[tag=db.member] {"text": "오버헤드킥! 준비 공을 사격하거나 착탄 예고 밖으로 이동하세요.", "color": "gold"}
execute if score #skill db.skill matches 5..6 at @e[tag=db.boss,limit=1] run function desert_ball:skills/core_spawn
