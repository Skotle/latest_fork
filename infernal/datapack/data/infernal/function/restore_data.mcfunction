$execute if entity @s[tag=inf.gear] run data modify entity @s equipment set from storage infernal:backup mobs."$(id)".equipment
$execute if entity @s[tag=inf.gear] run data modify entity @s drop_chances set from storage infernal:backup mobs."$(id)".drop_chances
$execute if entity @s[type=minecraft:creeper] run data modify entity @s Fuse set from storage infernal:backup mobs."$(id)".fuse
$data remove storage infernal:backup mobs."$(id)"
