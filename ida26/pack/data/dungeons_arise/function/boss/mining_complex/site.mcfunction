summon minecraft:marker ~ ~ ~ {"Tags":["ida.site","ida.site.mining_complex","ida.newsite"],"data":{"kind":"mining_complex","name":"깊은 갱도의 발파감독","hp":300,"color":"red","period":11,"primary":"blast","secondary":"reinforcements"}}
execute as @e[type=minecraft:marker,tag=ida.newsite,distance=..1,limit=1,sort=nearest] at @s run function dungeons_arise:boss/site/new
