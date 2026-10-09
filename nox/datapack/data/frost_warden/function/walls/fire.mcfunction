function frost_warden:arrows/normal
execute as @e[tag=fw.arrow] if score @s fw.id = #serial fw.id run tag @s add fw.wall_arrow
particle minecraft:snowflake ~ ~ ~ .1 .15 .1 0 5 force @a[tag=fw.active]
