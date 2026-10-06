function dungeons_arise:boss/bandit_towers/site
execute as @e[type=minecraft:marker,tag=ida.site.bandit_towers,distance=..1] if score @s ida.sid = #next ida.sid at @s run function dungeons_arise:boss/admin/start/bandit_towers
