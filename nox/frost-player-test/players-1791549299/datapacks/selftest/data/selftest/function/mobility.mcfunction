execute store result storage selftest:results mobility_restored int 1 run execute unless entity @a[tag=fw.stunned] unless entity @a[tag=fw.bound] unless entity @a[nbt={active_effects:[{id:"minecraft:slowness",amplifier:6b}]}]
execute as @a[tag=probe.player] run function frost_warden:stun/hit
execute store result storage selftest:results stun_guard int 1 run execute unless entity @a[tag=fw.stunned]
tp @a[tag=probe.player] 128 81 -8
execute as @a[tag=probe.player] at @s run function frost_warden:stun/apply
execute store result storage selftest:results stun_near int 1 run scoreboard players get @a[tag=probe.player,limit=1] fw.stun
execute as @a[tag=probe.player] run function frost_warden:stun/end
tp @a[tag=probe.player] 128 81 -12
execute as @a[tag=probe.player] at @s run function frost_warden:stun/apply
execute store result storage selftest:results stun_medium int 1 run scoreboard players get @a[tag=probe.player,limit=1] fw.stun
execute as @a[tag=probe.player] run function frost_warden:stun/end
tp @a[tag=probe.player] 128 81 -24
execute as @a[tag=probe.player] at @s run function frost_warden:stun/apply
execute store result storage selftest:results stun_far int 1 run scoreboard players get @a[tag=probe.player,limit=1] fw.stun
execute as @a[tag=probe.player] run function frost_warden:stun/end
tp @a[tag=probe.player] 128 81 -12
scoreboard players set #skill fw.skill 4
function frost_warden:skills/recover
execute store result storage selftest:results ultimate_recovery int 1 run scoreboard players get #safe fw.safe
scoreboard players set #time fw.time 1800
scoreboard players set #pool fw.hp 25000
scoreboard players set #safe fw.safe 0
scoreboard players set #next fw.next 0
scoreboard players set #cycle fw.cycle 0
scoreboard players set #focus fw.tmp 0
scoreboard players set #blink fw.blink 1
scoreboard players set #teleports fw.tmp 0
scoreboard objectives add probe.seen dummy
scoreboard players set #1 probe.seen 0
scoreboard players set #2 probe.seen 0
scoreboard players set #3 probe.seen 0
scoreboard players set #4 probe.seen 0
scoreboard players set #5 probe.seen 0
scoreboard players set #6 probe.seen 0
scoreboard players set #legacy_hazards probe.seen 0
