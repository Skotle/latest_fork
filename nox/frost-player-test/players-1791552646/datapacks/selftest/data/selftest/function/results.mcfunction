execute store result storage selftest:results walked int 1 run execute if score #steps fw.walk matches 20..
execute store result storage selftest:results seen_1 int 1 run scoreboard players get #1 probe.seen
execute store result storage selftest:results seen_2 int 1 run scoreboard players get #2 probe.seen
execute store result storage selftest:results seen_3 int 1 run scoreboard players get #3 probe.seen
execute store result storage selftest:results seen_4 int 1 run scoreboard players get #4 probe.seen
execute store result storage selftest:results seen_5 int 1 run scoreboard players get #5 probe.seen
execute store result storage selftest:results seen_6 int 1 run scoreboard players get #6 probe.seen
execute store result storage selftest:results legacy_hazards int 1 run scoreboard players get #legacy_hazards probe.seen
execute store result storage selftest:results no_permanent_slow int 1 run execute unless entity @a[tag=fw.bound] unless entity @a[nbt={active_effects:[{id:"minecraft:slowness",duration:-1}]}]
execute store result storage selftest:results phase int 1 run scoreboard players get #phase fw.phase
execute store result storage selftest:results adds int 1 run execute if entity @e[tag=fw.add]
execute store result storage selftest:results teleported int 1 run execute if score #teleports fw.tmp matches 1..
execute store result storage selftest:results sun_helmet int 1 run execute if items entity @e[tag=fw.boss,limit=1] armor.head minecraft:iron_helmet[minecraft:unbreakable]
scoreboard players add @a[tag=probe.player] nx.death 1
function frost_warden:fight/tick
execute store result storage selftest:results death_cleanup int 1 run execute unless entity @a[tag=fw.stunned] unless entity @a[tag=fw.bound]
scoreboard players operation @a[tag=probe.player] fw.olddeath = @a[tag=probe.player] nx.death
function frost_warden:fight/tick
function frost_warden:abort
execute store result storage selftest:results cleanup int 1 run execute unless entity @e[tag=fw.owned]
summon minecraft:arrow 128 82.5 5 {Tags:["probe.startarrow"],Motion:[0d,0d,-2d],pickup:0b,item:{id:"minecraft:arrow",count:1}}
