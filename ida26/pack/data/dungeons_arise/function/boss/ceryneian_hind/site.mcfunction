summon minecraft:marker ~ ~ ~ {"Tags":["ida.site","ida.site.ceryneian_hind","ida.newsite"],"data":{"kind":"ceryneian_hind","name":"금빛 모래의 사냥꾼","hp":220,"color":"yellow","period":11,"primary":"sandstorm","secondary":"charge"}}
execute as @e[type=minecraft:marker,tag=ida.newsite,distance=..1,limit=1,sort=nearest] at @s run function dungeons_arise:boss/site/new
