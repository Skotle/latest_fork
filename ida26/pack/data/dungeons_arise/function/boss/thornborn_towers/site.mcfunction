summon minecraft:marker ~ ~ ~ {"Tags":["ida.site","ida.site.thornborn_towers","ida.newsite"],"data":{"kind":"thornborn_towers","name":"가시탑의 썩은 군주","hp":320,"color":"red","period":12,"primary":"roots","secondary":"plague"}}
execute as @e[type=minecraft:marker,tag=ida.newsite,distance=..1,limit=1,sort=nearest] at @s run function dungeons_arise:boss/site/new
