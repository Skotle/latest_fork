tag @s add fw.current
tag @a[distance=..25,gamemode=!spectator] add fw.member
execute unless entity @a[tag=fw.member] run tag @s remove fw.current
execute if entity @a[tag=fw.member] run function frost_warden:fight/spawn
