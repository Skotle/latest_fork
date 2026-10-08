effect give @a[tag=nox.active,distance=..8] minecraft:resistance 6 0 true
effect give @a[tag=nox.active,distance=..8] minecraft:absorption 6 0 true
scoreboard players set #break nx.add 1
particle minecraft:totem_of_undying ~ ~1 ~ 2 .5 2 .1 18 force @a[tag=nox.member]
tellraw @a[tag=nox.member] {"text":"파수꾼의 종 파괴: 6초 저항·흡수. 다음 공격 종료 후 녹스 심장 2초 노출!","color":"gold"}
execute if entity @s[type=minecraft:player,tag=nox.active] run advancement grant @s only eclipse_nox:challenge/warden
execute if entity @s[type=minecraft:player,tag=nox.active] run scoreboard players add @s nx.warden 1
execute if entity @s[type=minecraft:player,tag=nox.active] if score @s nx.acolyte matches 1.. if score @s nx.warden matches 1.. run advancement grant @s only eclipse_nox:challenge/pair
