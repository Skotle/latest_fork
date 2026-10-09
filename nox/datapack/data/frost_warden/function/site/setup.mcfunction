setblock ~ ~1 ~ minecraft:target
summon minecraft:text_display ~ ~3.5 ~ {Tags:["fw.site_sign"],billboard:"center",text:{text:"서리의 파수꾼\n표적에 화살을 쏘면 결전 시작\n폭격 표식을 보면 즉시 이동",color:"aqua"}}
tag @s add fw.ready
