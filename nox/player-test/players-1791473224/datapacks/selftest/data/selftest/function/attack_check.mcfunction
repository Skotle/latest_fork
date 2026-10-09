execute store result storage selftest:results actual_hp int 1 run data get entity @e[tag=db.boss,limit=1] Health 100
execute store result storage selftest:results attack_refund int 1 run scoreboard players get @a[tag=probe.player,limit=1] db.debt
execute store result storage selftest:results refund_inventory_count int 1 run data get entity @a[tag=probe.player,limit=1] Inventory[{Slot:0b}].count
execute store result storage selftest:results refund_components int 1 run data get entity @a[tag=probe.player,limit=1] Inventory[{Slot:0b}].components."minecraft:custom_data".keep
execute store result storage selftest:results refund_vault_cleared int 1 run execute unless data storage desert_ball:vault accounts.p1
execute store result storage selftest:results boss_hurt int 1 run execute unless entity @e[tag=db.boss,nbt={Health:750f}]
scoreboard players set #safe db.safe 0
scoreboard players set #cast db.cast 40
scoreboard players set #skill db.skill 2
execute store result score #origin db.tmp run data get entity @e[tag=db.anchor,tag=db.current,limit=1] Pos[1] 100
execute as @e[tag=db.anchor,tag=db.current,limit=1] at @s run function desert_ball:skills/casting
execute store result score #y db.tmp run data get entity @e[tag=db.anchor,tag=db.current,limit=1] Pos[1] 100
scoreboard players operation #y db.tmp -= #origin db.tmp
execute store result storage selftest:results anchor_not_hidden int 1 run scoreboard players get #y db.tmp
execute store result score #y db.tmp run data get entity @e[tag=db.boss,limit=1] Pos[1] 100
scoreboard players operation #y db.tmp -= #origin db.tmp
execute store result storage selftest:results boss_hidden int 1 run scoreboard players get #y db.tmp
function desert_ball:skills/ambush_warn
function desert_ball:skills/resolve
scoreboard players set #cast db.cast 0
execute at @a[tag=probe.player,limit=1] store result storage selftest:results rear_ambush int 1 run execute if entity @e[tag=db.boss,distance=..4]
execute store result storage selftest:results chest_counter int 1 run execute if entity @e[tag=db.core]
damage @e[tag=db.core,limit=1] 2 minecraft:generic
function desert_ball:skills/core_tick
