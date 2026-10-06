function dungeons_arise:boss/infested_temple/site
execute as @e[type=minecraft:marker,tag=ida.site.infested_temple,distance=..1] if score @s ida.sid = #next ida.sid at @s run function dungeons_arise:boss/admin/start/infested_temple
