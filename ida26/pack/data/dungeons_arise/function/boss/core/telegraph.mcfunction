$execute if score @s ida.skill matches 0 run function dungeons_arise:boss/spell/$(primary)/telegraph with entity @s data
$execute if score @s ida.skill matches 1 run function dungeons_arise:boss/spell/$(secondary)/telegraph with entity @s data
