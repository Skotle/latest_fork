attribute @a[tag=probe.player,limit=1] minecraft:knockback_resistance base set 1
summon minecraft:pig 130 81 -6 {Tags:["probe.attacker"],NoAI:1b,NoGravity:1b,PersistenceRequired:1b}
tag @a[tag=probe.player] add probe.armor_sample
tag @a[tag=probe.player] add probe.shield
tag @a[tag=probe.player] add probe.heal
item replace entity @a[tag=probe.player,limit=1] armor.head with minecraft:leather_helmet
