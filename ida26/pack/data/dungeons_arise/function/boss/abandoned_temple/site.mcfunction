summon minecraft:marker ~ ~ ~ {"Tags":["ida.site","ida.site.abandoned_temple","ida.newsite"],"data":{"kind":"abandoned_temple","name":"잊힌 사원의 독니","hp":180,"color":"red","period":10,"primary":"venom","secondary":"fangs"}}
execute as @e[type=minecraft:marker,tag=ida.newsite,distance=..1,limit=1,sort=nearest] at @s run function dungeons_arise:boss/site/new
