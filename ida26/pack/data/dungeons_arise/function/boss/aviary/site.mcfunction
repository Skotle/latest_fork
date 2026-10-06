summon minecraft:marker ~ ~ ~ {"Tags":["ida.site","ida.site.aviary","ida.newsite"],"data":{"kind":"aviary","name":"철창 위의 폭풍날개","hp":200,"color":"red","period":11,"primary":"gale","secondary":"snipe"}}
execute as @e[type=minecraft:marker,tag=ida.newsite,distance=..1,limit=1,sort=nearest] at @s run function dungeons_arise:boss/site/new
