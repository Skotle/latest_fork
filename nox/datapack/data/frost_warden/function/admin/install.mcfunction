execute if dimension minecraft:overworld if score #state fw.state matches 0 run place template frost_warden:watchtower ~-17 ~-2 ~-17
execute as @e[tag=fw.site_seed,distance=..3] at @s run function frost_warden:site/init
