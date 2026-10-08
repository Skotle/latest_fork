effect give @a[tag=nox.active,distance=..8] minecraft:instant_health 1 0 true
effect give @a[tag=nox.active,distance=..8] minecraft:regeneration 5 0 true
effect give @a[tag=nox.active,distance=..8] minecraft:speed 5 0 true
particle minecraft:heart ~ ~1 ~ 2 .5 2 0 14 force @a[tag=nox.member]
tellraw @a[tag=nox.active,distance=..8] {"text":"시종의 잔향: 체력 회복 + 5초 재생·신속!","color":"aqua"}
execute if entity @s[type=minecraft:player,tag=nox.active] run advancement grant @s only eclipse_nox:challenge/acolyte
execute if entity @s[type=minecraft:player,tag=nox.active] run scoreboard players add @s nx.acolyte 1
execute if entity @s[type=minecraft:player,tag=nox.active] if score @s nx.acolyte matches 1.. if score @s nx.warden matches 1.. run advancement grant @s only eclipse_nox:challenge/pair
