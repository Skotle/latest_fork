summon minecraft:marker ~ ~ ~ {"Tags":["ida.site","ida.site.heavenly_rider","ida.newsite"],"data":{"kind":"heavenly_rider","name":"별바람의 기수","hp":300,"color":"purple","period":10,"primary":"gale","secondary":"starfall"}}
execute as @e[type=minecraft:marker,tag=ida.newsite,distance=..1,limit=1,sort=nearest] at @s run function dungeons_arise:boss/site/new
