function dungeons_arise:boss/heavenly_challenger/site
execute as @e[type=minecraft:marker,tag=ida.site.heavenly_challenger,distance=..1] if score @s ida.sid = #next ida.sid at @s run function dungeons_arise:boss/admin/start/heavenly_challenger
