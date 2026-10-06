scoreboard players set @s ida.phase 2
$bossbar set dungeons_arise:encounter_$(id) color red
$tellraw @a[distance=..64] {"text":"[IDA] $(name)이(가) 격노했습니다! 공격 주기가 빨라집니다.","color":"red"}
playsound minecraft:entity.ravager.roar hostile @a[distance=..64] ~ ~ ~ 0.7 0.8
particle minecraft:angry_villager ~ ~2 ~ 0.5 0.5 0.5 0 25 force
