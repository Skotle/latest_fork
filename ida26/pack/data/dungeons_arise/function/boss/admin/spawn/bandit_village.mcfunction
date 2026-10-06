function dungeons_arise:boss/bandit_village/site
execute as @e[type=minecraft:marker,tag=ida.site.bandit_village,distance=..1] if score @s ida.sid = #next ida.sid at @s run function dungeons_arise:boss/admin/start/bandit_village
