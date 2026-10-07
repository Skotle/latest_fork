tag @s remove nox.seed
tag @s add nox.anchor
tag @s add nox.site
scoreboard players set #installed nx.state 1
scoreboard players add #site nx.tmp 1
scoreboard players operation @s nx.tmp = #site nx.tmp
setblock ~0 ~0 ~-20 minecraft:lodestone
execute positioned ~0 ~1 ~-20 run summon minecraft:item_display ~ ~ ~ {"Tags":["nox.owned","nox.visual","nox.bell","nox.bell1"],"Invulnerable":true,"item":{"id":"minecraft:paper","count":1,"components":{"minecraft:item_model":"eclipse_nox:bell"}},"item_display":"fixed","view_range":2.0,"teleport_duration":1,"interpolation_duration":5,"brightness":{"block":12,"sky":12},"transformation":{"translation":[0,0.5,0],"scale":[1,1,1],"left_rotation":[0,0,0,1],"right_rotation":[0,0,0,1]}}
summon minecraft:interaction ~0 ~1 ~-20 {Tags:["nox.owned","nox.bell","nox.bell1"],width:2f,height:2f,response:1b}
summon minecraft:text_display ~0 ~3 ~-20 {Tags:["nox.owned"],billboard:"center",text:{text:"봉인종 1",color:"gold"}}
setblock ~-17 ~0 ~10 minecraft:lodestone
execute positioned ~-17 ~1 ~10 run summon minecraft:item_display ~ ~ ~ {"Tags":["nox.owned","nox.visual","nox.bell","nox.bell2"],"Invulnerable":true,"item":{"id":"minecraft:paper","count":1,"components":{"minecraft:item_model":"eclipse_nox:bell"}},"item_display":"fixed","view_range":2.0,"teleport_duration":1,"interpolation_duration":5,"brightness":{"block":12,"sky":12},"transformation":{"translation":[0,0.5,0],"scale":[1,1,1],"left_rotation":[0,0,0,1],"right_rotation":[0,0,0,1]}}
summon minecraft:interaction ~-17 ~1 ~10 {Tags:["nox.owned","nox.bell","nox.bell2"],width:2f,height:2f,response:1b}
summon minecraft:text_display ~-17 ~3 ~10 {Tags:["nox.owned"],billboard:"center",text:{text:"봉인종 2",color:"gold"}}
setblock ~17 ~0 ~10 minecraft:lodestone
execute positioned ~17 ~1 ~10 run summon minecraft:item_display ~ ~ ~ {"Tags":["nox.owned","nox.visual","nox.bell","nox.bell3"],"Invulnerable":true,"item":{"id":"minecraft:paper","count":1,"components":{"minecraft:item_model":"eclipse_nox:bell"}},"item_display":"fixed","view_range":2.0,"teleport_duration":1,"interpolation_duration":5,"brightness":{"block":12,"sky":12},"transformation":{"translation":[0,0.5,0],"scale":[1,1,1],"left_rotation":[0,0,0,1],"right_rotation":[0,0,0,1]}}
summon minecraft:interaction ~17 ~1 ~10 {Tags:["nox.owned","nox.bell","nox.bell3"],width:2f,height:2f,response:1b}
summon minecraft:text_display ~17 ~3 ~10 {Tags:["nox.owned"],billboard:"center",text:{text:"봉인종 3",color:"gold"}}
execute positioned ~0 ~0 ~29 run summon minecraft:item_display ~ ~ ~ {"Tags":["nox.owned","nox.visual","nox.device"],"Invulnerable":true,"item":{"id":"minecraft:paper","count":1,"components":{"minecraft:item_model":"eclipse_nox:device"}},"item_display":"fixed","view_range":2.0,"teleport_duration":1,"interpolation_duration":5,"brightness":{"block":12,"sky":12},"transformation":{"translation":[0,1,0],"scale":[1,1,1],"left_rotation":[0,0,0,1],"right_rotation":[0,0,0,1]}}
summon minecraft:interaction ~0 ~0 ~29 {Tags:["nox.owned","nox.start"],width:2f,height:2f,response:1b}
summon minecraft:text_display ~0 ~2.5 ~29 {Tags:["nox.owned"],billboard:"center",line_width:240,text:{text:"일식 관측소\n종을 우클릭하여 전투 시작\n순서: 북쪽 1 → 동쪽 3 → 서쪽 2\n입구 뒤에서 준비 후 중앙으로 진입",color:"gold"}}
function eclipse_nox:arena/decorate
