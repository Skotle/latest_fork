summon minecraft:marker ~ ~ ~ {"Tags":["ida.site","ida.site.bathhouse","ida.newsite"],"data":{"kind":"bathhouse","name":"침수된 목욕장의 파수꾼","hp":200,"color":"blue","period":11,"primary":"tide","secondary":"frost"}}
execute as @e[type=minecraft:marker,tag=ida.newsite,distance=..1,limit=1,sort=nearest] at @s run function dungeons_arise:boss/site/new
