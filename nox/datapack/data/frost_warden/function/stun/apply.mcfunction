tag @s add fw.stunned
scoreboard players set @s fw.stun 30
execute at @s if entity @e[tag=fw.boss,distance=..18] run scoreboard players set @s fw.stun 20
execute at @s if entity @e[tag=fw.boss,distance=..8] run scoreboard players set @s fw.stun 10
scoreboard players set @s fw.guard 80
effect give @s minecraft:slowness 1 6 true
effect give @a[tag=fw.active,distance=..2] minecraft:slowness 1 0 true
tellraw @s {text:"수정화살에 피격! 짧은 기절 후 이동이 회복됩니다.",color:"aqua"}
