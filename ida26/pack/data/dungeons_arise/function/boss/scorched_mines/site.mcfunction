summon minecraft:marker ~ ~ ~ {"Tags":["ida.site","ida.site.scorched_mines","ida.newsite"],"data":{"kind":"scorched_mines","name":"그을린 갱도의 잿빛 추적자","hp":280,"color":"red","period":11,"primary":"forge","secondary":"charge"}}
execute as @e[type=minecraft:marker,tag=ida.newsite,distance=..1,limit=1,sort=nearest] at @s run function dungeons_arise:boss/site/new
