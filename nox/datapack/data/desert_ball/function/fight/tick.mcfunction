tag @a remove db.active
execute as @a[tag=db.member,distance=..38,gamemode=!spectator] if score @s nx.death = @s db.olddeath if score @s nx.leave = @s db.oldleave run tag @s add db.active
execute unless entity @a[tag=db.active] run scoreboard players add #idle db.idle 1
execute if entity @a[tag=db.active] run scoreboard players set #idle db.idle 0
execute if score #idle db.idle matches 100.. run function desert_ball:abort
execute if score #state db.state matches 1 if score #idle db.idle matches ..99 unless entity @e[tag=db.boss] run function desert_ball:victory
execute if score #state db.state matches 1 if entity @e[tag=db.boss] run function desert_ball:fight/alive
