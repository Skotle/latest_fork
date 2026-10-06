summon minecraft:marker ~ ~ ~ {"Tags":["ida.site","ida.site.typhon","ida.newsite"],"data":{"kind":"typhon","name":"심해의 폭풍왕 티폰","hp":380,"color":"blue","period":11,"primary":"tide","secondary":"thunder"}}
execute as @e[type=minecraft:marker,tag=ida.newsite,distance=..1,limit=1,sort=nearest] at @s run function dungeons_arise:boss/site/new
