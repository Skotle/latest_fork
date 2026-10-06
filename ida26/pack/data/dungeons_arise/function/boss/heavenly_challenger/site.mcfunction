summon minecraft:marker ~ ~ ~ {"Tags":["ida.site","ida.site.heavenly_challenger","ida.newsite"],"data":{"kind":"heavenly_challenger","name":"천공의 시험관","hp":280,"color":"purple","period":11,"primary":"gale","secondary":"void"}}
execute as @e[type=minecraft:marker,tag=ida.newsite,distance=..1,limit=1,sort=nearest] at @s run function dungeons_arise:boss/site/new
