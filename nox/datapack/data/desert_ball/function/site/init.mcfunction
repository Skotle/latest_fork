tag @s remove db.seed
tag @s add db.anchor
execute positioned ~0 ~0 ~35 run summon minecraft:interaction ~ ~ ~ {Tags:["db.owned","db.start"],width:2f,height:2f,response:1b}
summon minecraft:text_display ~0 ~3 ~35 {Tags:["db.owned"],billboard:"center",text:{text:"사막의 베르나베우\n우클릭: 크리스티아누\n활·석궁 권장 / 도난품은 자동 반환",color:"gold"}}
