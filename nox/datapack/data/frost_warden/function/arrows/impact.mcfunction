scoreboard players operation #id fw.id = @s fw.id
execute as @e[tag=fw.tracker] if score @s fw.id = #id fw.id run kill @s
execute rotated as @s positioned ^ ^ ^-.2 positioned ~ ~.2 ~ run function frost_warden:explosion
kill @s
