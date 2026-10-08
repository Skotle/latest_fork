execute store result storage desert_ball:ctx owner int 1 run scoreboard players get @s db.owner
function desert_ball:theft/read with storage desert_ball:ctx
execute store success score #returned db.tmp run function desert_ball:theft/drop with storage desert_ball:capture
execute if score #returned db.tmp matches 1 run function desert_ball:theft/delete with storage desert_ball:ctx
execute if score #returned db.tmp matches 1 run scoreboard players set @s db.debt 0
