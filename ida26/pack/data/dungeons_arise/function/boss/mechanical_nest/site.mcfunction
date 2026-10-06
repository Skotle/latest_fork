summon minecraft:marker ~ ~ ~ {"Tags":["ida.site","ida.site.mechanical_nest","ida.newsite"],"data":{"kind":"mechanical_nest","name":"기계 둥지의 전류감독","hp":340,"color":"red","period":10,"primary":"thunder","secondary":"snipe"}}
execute as @e[type=minecraft:marker,tag=ida.newsite,distance=..1,limit=1,sort=nearest] at @s run function dungeons_arise:boss/site/new
