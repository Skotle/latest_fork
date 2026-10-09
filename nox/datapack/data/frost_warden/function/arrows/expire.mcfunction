scoreboard players operation #id fw.id = @s fw.id
execute as @e[tag=fw.tracker] if score @s fw.id = #id fw.id run kill @s
kill @s
