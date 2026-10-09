kill @e[tag=fw.ray_target]
execute at @s run summon minecraft:marker ~ ~1 ~ {Tags:["fw.ray_target"]}
scoreboard players set #ray fw.tmp 0
execute facing entity @e[tag=fw.ray_target,limit=1] feet run function frost_warden:explosion/ray
kill @e[tag=fw.ray_target]
