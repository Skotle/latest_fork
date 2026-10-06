summon minecraft:marker ~ ~ ~ {"Tags":["ida.site","ida.site.heavenly_conqueror","ida.newsite"],"data":{"kind":"heavenly_conqueror","name":"공허의 정복자","hp":440,"color":"purple","period":11,"primary":"void","secondary":"thunder"}}
execute as @e[type=minecraft:marker,tag=ida.newsite,distance=..1,limit=1,sort=nearest] at @s run function dungeons_arise:boss/site/new
