tag @s add db.current
tag @a[distance=..38,gamemode=!spectator,tag=!nox.member] add db.member
execute unless entity @a[tag=db.member] run tag @s remove db.current
execute if entity @a[tag=db.member] run function desert_ball:fight/spawn
