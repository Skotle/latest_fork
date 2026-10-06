summon minecraft:marker ~ ~ ~ {"Tags":["ida.site","ida.site.bandit_village","ida.newsite"],"data":{"kind":"bandit_village","name":"약탈왕 붉은송곳","hp":260,"color":"red","period":11,"primary":"cleave","secondary":"reinforcements"}}
execute as @e[type=minecraft:marker,tag=ida.newsite,distance=..1,limit=1,sort=nearest] at @s run function dungeons_arise:boss/site/new
