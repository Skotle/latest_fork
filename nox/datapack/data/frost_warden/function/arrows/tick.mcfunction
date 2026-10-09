scoreboard players remove @s fw.age 1
execute if entity @s[tag=fw.explosive] run particle minecraft:flame ~ ~ ~ .04 .04 .04 0 2 force @a[tag=fw.active]
execute if entity @s[tag=fw.explosive,nbt={inGround:1b}] run function frost_warden:arrows/impact
execute if entity @s[tag=!fw.explosive,nbt={inGround:1b}] run kill @s
execute if score @s fw.age matches ..0 run function frost_warden:arrows/expire
