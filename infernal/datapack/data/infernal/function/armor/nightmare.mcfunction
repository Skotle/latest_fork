execute store result score #parts inf.sys run random value 2..4
execute store result score #order inf.sys run random value 0..3
execute if score #order inf.sys matches 0 run function infernal:armor/nightmare_0
execute if score #order inf.sys matches 1 run function infernal:armor/nightmare_1
execute if score #order inf.sys matches 2 run function infernal:armor/nightmare_2
execute if score #order inf.sys matches 3 run function infernal:armor/nightmare_3
