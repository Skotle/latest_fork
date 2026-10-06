scoreboard players set @s ida.stage 2
scoreboard players set @s ida.cool 0
$advancement grant @a[predicate=dungeons_arise:boss/eligible,distance=..96] only dungeons_arise:boss/$(kind)
$tellraw @a[distance=..96] {"text":"[IDA] $(name) 격파! 보스가 있던 위치에서 전용 보상을 회수하세요.","color":"gold"}
playsound minecraft:ui.toast.challenge_complete master @a[distance=..96] ~ ~ ~ 0.6 1
function dungeons_arise:boss/site/cleanup with entity @s data
