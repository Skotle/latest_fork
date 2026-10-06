summon minecraft:marker ~ ~ ~ {"Tags":["ida.site","ida.site.plague_asylum","ida.newsite"],"data":{"kind":"plague_asylum","name":"역병 수용소의 원장","hp":440,"color":"purple","period":12,"primary":"plague","secondary":"soul"}}
execute as @e[type=minecraft:marker,tag=ida.newsite,distance=..1,limit=1,sort=nearest] at @s run function dungeons_arise:boss/site/new
