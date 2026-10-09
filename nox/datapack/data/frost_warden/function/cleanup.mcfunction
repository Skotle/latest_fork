execute if data storage frost_warden:ctx owner run function frost_warden:arrows/native with storage frost_warden:ctx
execute as @e[tag=fw.add] run function frost_warden:arrows/add_scan
kill @e[tag=fw.owned]
kill @e[tag=fw.vector]
kill @e[tag=fw.ray_target]
tag @a remove fw.member
tag @a remove fw.active
tag @e[tag=fw.current] remove fw.current
bossbar set frost_warden:health visible false
scoreboard players set #cast fw.cast 0
execute as @a[tag=fw.revealed] run effect clear @s minecraft:glowing
tag @a remove fw.revealed
scoreboard players set @a fw.guard 0
