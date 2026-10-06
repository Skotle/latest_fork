summon minecraft:marker ~ ~ ~ {"Tags":["ida.site","ida.site.foundry","ida.newsite"],"data":{"kind":"foundry","name":"용광로의 검은 대장장이","hp":340,"color":"red","period":11,"primary":"forge","secondary":"reinforcements"}}
execute as @e[type=minecraft:marker,tag=ida.newsite,distance=..1,limit=1,sort=nearest] at @s run function dungeons_arise:boss/site/new
