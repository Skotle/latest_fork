function dungeons_arise:boss/scorched_mines/site
execute as @e[type=minecraft:marker,tag=ida.site.scorched_mines,distance=..1] if score @s ida.sid = #next ida.sid at @s run function dungeons_arise:boss/admin/start/scorched_mines
