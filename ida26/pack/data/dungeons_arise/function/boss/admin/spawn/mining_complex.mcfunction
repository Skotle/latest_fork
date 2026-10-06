function dungeons_arise:boss/mining_complex/site
execute as @e[type=minecraft:marker,tag=ida.site.mining_complex,distance=..1] if score @s ida.sid = #next ida.sid at @s run function dungeons_arise:boss/admin/start/mining_complex
