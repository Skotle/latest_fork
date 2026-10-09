scoreboard players set #safe db.safe 0
scoreboard players set #cast db.cast 40
scoreboard players set #skill db.skill 3
function desert_ball:skills/noshow
function desert_ball:skills/noshow
execute store result storage selftest:results decoys_bounded int 1 run execute if entity @e[tag=db.decoy]
function desert_ball:visual/tick
execute store result score #ballscale db.tmp run data get entity @e[tag=db.carried_ball,limit=1] transformation.scale[0] 100
execute store result storage selftest:results real_ball_visible int 1 run execute if score #ballscale db.tmp matches 100..120
function desert_ball:skills/resolve
execute store result storage selftest:results decoys_expired int 1 run execute unless entity @e[tag=db.decoy]
scoreboard players set #cast db.cast 0
execute store result storage selftest:results before_hit int 1 run data get entity @a[tag=probe.player,limit=1] Health 10
