scoreboard players add #walk fw.walk 1
execute if score #walk fw.walk matches 80.. run scoreboard players set #walk fw.walk 0
execute if score #safe fw.safe matches 0..24 unless score #skill fw.skill matches 4 as @e[tag=fw.boss,limit=1] at @s if entity @a[tag=fw.active,gamemode=!creative] run function frost_warden:movement/choose
execute if score #skill fw.skill matches 4 if score #cast fw.cast matches 0 if score #safe fw.safe matches 0 as @e[tag=fw.boss,limit=1] at @s if entity @a[tag=fw.active,gamemode=!creative] run function frost_warden:movement/choose
