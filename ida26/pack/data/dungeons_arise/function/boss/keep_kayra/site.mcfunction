summon minecraft:marker ~ ~ ~ {"Tags":["ida.site","ida.site.keep_kayra","ida.newsite"],"data":{"kind":"keep_kayra","name":"카이라의 늪지 기사","hp":400,"color":"red","period":12,"primary":"cleave","secondary":"tide"}}
execute as @e[type=minecraft:marker,tag=ida.newsite,distance=..1,limit=1,sort=nearest] at @s run function dungeons_arise:boss/site/new
