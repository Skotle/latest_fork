advancement revoke @s only desert_ball:internal/hit
execute if entity @s[tag=db.active] if score #state db.state matches 1 as @a[scores={db.debt=1}] at @s run function desert_ball:theft/return
execute if score #skill db.skill matches 3 run kill @e[tag=db.decoy]
