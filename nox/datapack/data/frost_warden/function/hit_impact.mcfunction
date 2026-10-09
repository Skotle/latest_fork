execute as @e[tag=fw.explosive,distance=..6,sort=nearest,limit=1] run function frost_warden:arrows/expire
execute positioned ~ ~1 ~ run function frost_warden:explosion
