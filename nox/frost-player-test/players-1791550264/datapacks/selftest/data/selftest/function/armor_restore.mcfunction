execute store result storage selftest:results full_boss_after int 1 run data get entity @a[tag=probe.player,limit=1] Health 1000
item replace entity @a[tag=probe.player,limit=1] armor.head with minecraft:air
item replace entity @a[tag=probe.player,limit=1] armor.chest with minecraft:air
item replace entity @a[tag=probe.player,limit=1] armor.legs with minecraft:air
item replace entity @a[tag=probe.player,limit=1] armor.feet with minecraft:air
tag @a[tag=probe.player] add probe.heal
tag @a[tag=probe.player] remove probe.shield
kill @e[tag=probe.attacker]
