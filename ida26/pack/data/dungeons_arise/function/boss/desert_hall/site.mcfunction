summon minecraft:marker ~ ~ ~ {"Tags":["ida.site","ida.site.desert_hall","ida.newsite"],"data":{"kind":"desert_hall","name":"태양왕 아케트","hp":360,"color":"yellow","period":12,"primary":"sunfire","secondary":"sandstorm"}}
execute as @e[type=minecraft:marker,tag=ida.newsite,distance=..1,limit=1,sort=nearest] at @s run function dungeons_arise:boss/site/new
