scoreboard players set #moving nx.move 0
execute if score #cast nx.cast matches 0 if score #dash nx.dash matches 0 if score #safe nx.safe matches 0 if score #puzzle nx.puzzle matches 0 as @e[tag=nox.boss,limit=1] at @s facing entity @a[tag=nox.active,sort=nearest,limit=1] feet run function eclipse_nox:fight/step
