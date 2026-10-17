data modify entity @s equipment.mainhand set value {id:"minecraft:iron_sword",count:1,components:{"minecraft:enchantments":{"minecraft:sharpness":2}}}
data modify entity @s drop_chances.mainhand set value 0.0f
tag @s add inf.gear
execute store result score #rare inf.sys run random value 1..100
execute if score #rare inf.sys matches ..5 run function infernal:weapon/nightmare_diamond
