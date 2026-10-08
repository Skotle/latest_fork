scoreboard players operation #ballid db.owner = @s db.owner
execute as @e[tag=db.shot_visual] if score @s db.owner = #ballid db.owner run kill @s
kill @s
