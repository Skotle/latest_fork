summon minecraft:marker ~ ~ ~ {"Tags":["ida.site","ida.site.bandit_towers","ida.newsite"],"data":{"kind":"bandit_towers","name":"붉은 절벽의 저격수","hp":200,"color":"red","period":10,"primary":"snipe","secondary":"reinforcements"}}
execute as @e[type=minecraft:marker,tag=ida.newsite,distance=..1,limit=1,sort=nearest] at @s run function dungeons_arise:boss/site/new
