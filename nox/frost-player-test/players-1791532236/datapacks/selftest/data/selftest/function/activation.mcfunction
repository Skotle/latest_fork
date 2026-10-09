execute store result storage selftest:results target_start int 1 run execute if entity @e[tag=fw.boss]
summon minecraft:marker 128 81 0 {Tags:["db.anchor","db.ready","probe.dummy"]}
execute positioned 128 81 0 run function desert_ball:admin/summon
execute store result storage selftest:results other_boss_blocked int 1 run execute unless entity @e[tag=db.boss]
execute as @e[tag=fw.anchor,limit=1] at @s run function eclipse_nox:fight/start
execute store result storage selftest:results nox_blocked int 1 run scoreboard players get #state nx.state
kill @e[tag=probe.dummy]
scoreboard players set @a[tag=probe.player] fw.hits 0
scoreboard players set @a[tag=probe.player] fw.shield 0
scoreboard players set #pool fw.hp 0
