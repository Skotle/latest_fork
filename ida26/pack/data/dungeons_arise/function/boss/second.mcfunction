execute store result score #difficulty ida.tmp run difficulty
execute if score #enabled ida.cfg matches 1 if score #difficulty ida.tmp matches 1.. as @a[predicate=dungeons_arise:boss/eligible] at @s run function dungeons_arise:boss/detect
execute in minecraft:overworld run function dungeons_arise:boss/dimension
execute in minecraft:the_nether run function dungeons_arise:boss/dimension
execute in minecraft:the_end run function dungeons_arise:boss/dimension
