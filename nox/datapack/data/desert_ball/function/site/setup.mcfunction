kill @e[type=minecraft:interaction,tag=db.start,distance=..38]
kill @e[type=minecraft:text_display,tag=db.owned,distance=..40]
setblock ~ ~-1 ~ minecraft:gold_block
summon minecraft:interaction ~ ~ ~ {Tags:["db.owned","db.start"],width:2f,height:2f,response:1b}
summon minecraft:text_display ~ ~3 ~ {Tags:["db.owned","db.sign"],billboard:"center",text:{text:"크리스티아누 소환대\n금색 블록 바로 위를 우클릭\n활·석궁 권장",color:"gold"}}
tag @s add db.ready
