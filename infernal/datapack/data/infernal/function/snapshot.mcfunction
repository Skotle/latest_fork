$data modify storage infernal:backup mobs."$(id)" set value {equipment:{},drop_chances:{}}
$data modify storage infernal:backup mobs."$(id)".equipment set from entity @s equipment
$data modify storage infernal:backup mobs."$(id)".drop_chances set from entity @s drop_chances
$data modify storage infernal:backup mobs."$(id)".fuse set from entity @s Fuse
