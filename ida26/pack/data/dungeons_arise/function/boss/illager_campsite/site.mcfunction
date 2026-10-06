summon minecraft:marker ~ ~ ~ {"Tags":["ida.site","ida.site.illager_campsite","ida.newsite"],"data":{"kind":"illager_campsite","name":"야영지의 돌격대장","hp":160,"color":"red","period":12,"primary":"charge","secondary":"reinforcements"}}
execute as @e[type=minecraft:marker,tag=ida.newsite,distance=..1,limit=1,sort=nearest] at @s run function dungeons_arise:boss/site/new
