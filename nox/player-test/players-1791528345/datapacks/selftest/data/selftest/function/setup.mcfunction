forceload add 96 -48 160 48
execute positioned 128 81 0 run function desert_ball:admin/install
execute positioned 128 81 0 run function desert_ball:admin/summon
execute store result storage selftest:results member int 1 run execute if entity @a[tag=db.member]
execute store result storage selftest:results health int 1 run data get entity @e[tag=db.boss,limit=1] Health
execute as @e[tag=db.anchor,tag=db.current] at @s run function desert_ball:fight/tick
execute store result storage selftest:results active int 1 run execute if entity @a[tag=db.active]
scoreboard players set #next db.next 9999
scoreboard players set #time db.time 100
clear @a[tag=probe.player]
item replace entity @a[tag=probe.player,limit=1] weapon.mainhand with minecraft:diamond[minecraft:custom_data={keep:73}] 3
execute as @a[tag=probe.player] at @s run function desert_ball:theft/attempt
execute store result storage selftest:results debt int 1 run scoreboard players get @a[tag=probe.player,limit=1] db.debt
execute store result storage selftest:results remaining int 1 run data get entity @a[tag=probe.player,limit=1] Inventory[{Slot:0b}].count
execute store result storage selftest:results kept_components int 1 run data get entity @a[tag=probe.player,limit=1] Inventory[{Slot:0b}].components."minecraft:custom_data".keep
tag @a[tag=probe.player] add probe.attack
