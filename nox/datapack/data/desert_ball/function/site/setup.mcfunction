kill @e[type=minecraft:interaction,tag=db.start,distance=..38]
kill @e[type=minecraft:text_display,tag=db.owned,distance=..40]
setblock ~ ~-1 ~ minecraft:gold_block
summon minecraft:text_display ~ ~3 ~ {Tags:["db.owned","db.sign"],billboard:"center",text:{text:"실험용 경기장 — 치트 전용\n/function desert_ball:admin/summon",color:"gray"}}
tag @s add db.ready
