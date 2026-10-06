summon minecraft:marker ~ ~ ~ {"Tags":["ida.site","ida.site.small_blimp","ida.newsite"],"data":{"kind":"small_blimp","name":"비행선장 구름갈퀴","hp":180,"color":"red","period":11,"primary":"snipe","secondary":"gale"}}
execute as @e[type=minecraft:marker,tag=ida.newsite,distance=..1,limit=1,sort=nearest] at @s run function dungeons_arise:boss/site/new
