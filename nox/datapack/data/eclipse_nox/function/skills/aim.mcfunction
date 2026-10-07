execute as @e[tag=nox.boss,limit=1] at @s facing entity @a[tag=nox.active,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute at @e[tag=nox.boss,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["nox.owned","nox.target"]}
execute as @e[tag=nox.target,limit=1] at @s rotated as @e[tag=nox.boss,limit=1] run tp @s ~ ~ ~ ~ 0
