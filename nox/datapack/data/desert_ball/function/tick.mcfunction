execute as @e[tag=db.seed] at @s if entity @a[distance=..100] run function desert_ball:site/init
execute if score #state db.state matches 0 as @e[tag=db.start] at @s if data entity @s interaction run function desert_ball:start
execute if score #state db.state matches 1 as @e[tag=db.anchor,tag=db.current,limit=1] at @s run function desert_ball:fight/tick
execute if score #state db.state matches 1 unless entity @e[tag=db.anchor,tag=db.current] run function desert_ball:abort
