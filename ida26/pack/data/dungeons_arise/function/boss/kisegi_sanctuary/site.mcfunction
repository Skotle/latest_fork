summon minecraft:marker ~ ~ ~ {"Tags":["ida.site","ida.site.kisegi_sanctuary","ida.newsite"],"data":{"kind":"kisegi_sanctuary","name":"키세기의 비단 여왕","hp":360,"color":"red","period":11,"primary":"web","secondary":"fangs"}}
execute as @e[type=minecraft:marker,tag=ida.newsite,distance=..1,limit=1,sort=nearest] at @s run function dungeons_arise:boss/site/new
