effect give @a[tag=nox.active,distance=..8] minecraft:instant_health 1 0 true
effect give @a[tag=nox.active,distance=..8] minecraft:regeneration 5 0 true
effect give @a[tag=nox.active,distance=..8] minecraft:speed 5 0 true
particle minecraft:heart ~ ~1 ~ 2 .5 2 0 14 force @a[tag=nox.member]
tellraw @a[tag=nox.active,distance=..8] {"text":"시종의 잔향: 체력 회복 + 5초 재생·신속!","color":"aqua"}
