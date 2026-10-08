data remove entity @s interaction
execute if score #state nx.state matches 0 if score #state db.state matches 0 as @e[tag=db.anchor,distance=..38,sort=nearest,limit=1] at @s run function desert_ball:begin
