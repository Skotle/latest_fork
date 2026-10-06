summon minecraft:marker ~ ~ ~ {"Tags":["ida.site","ida.site.infested_temple","ida.newsite"],"data":{"kind":"infested_temple","name":"서리 역병의 사제","hp":320,"color":"blue","period":11,"primary":"frost","secondary":"plague"}}
execute as @e[type=minecraft:marker,tag=ida.newsite,distance=..1,limit=1,sort=nearest] at @s run function dungeons_arise:boss/site/new
