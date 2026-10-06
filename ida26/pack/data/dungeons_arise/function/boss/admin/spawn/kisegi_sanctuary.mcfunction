function dungeons_arise:boss/kisegi_sanctuary/site
execute as @e[type=minecraft:marker,tag=ida.site.kisegi_sanctuary,distance=..1] if score @s ida.sid = #next ida.sid at @s run function dungeons_arise:boss/admin/start/kisegi_sanctuary
