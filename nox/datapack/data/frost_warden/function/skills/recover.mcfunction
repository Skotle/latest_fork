scoreboard players set #safe fw.safe 10
execute if score #skill fw.skill matches 3 run scoreboard players set #safe fw.safe 6
execute if score #skill fw.skill matches 6 run scoreboard players set #safe fw.safe 6
execute if score #skill fw.skill matches 4 run scoreboard players set #safe fw.safe 24
kill @e[tag=fw.aim]
data merge entity @e[tag=fw.boss,limit=1] {NoAI:1b}
tellraw @a[tag=fw.member] {"text": "장전 중! 반격하세요.", "color": "aqua"}
