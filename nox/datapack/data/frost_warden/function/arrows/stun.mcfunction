function frost_warden:arrows/normal
execute as @e[tag=fw.arrow] if score @s fw.id = #serial fw.id run tag @s add fw.stun_arrow
execute as @e[tag=fw.stun_arrow] if score @s fw.id = #serial fw.id run data merge entity @s {damage:6.5d,PierceLevel:1b}
