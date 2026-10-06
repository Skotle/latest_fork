tp @s ~ ~ ~
data modify entity @s Motion set value [0.0d,0.0d,0.0d]
execute if entity @s[tag=ida.boss] run scoreboard players set @s ida.stage 0
execute if entity @s[tag=ida.boss] run scoreboard players set @s ida.wind 0
execute if entity @s[tag=ida.boss] run scoreboard players set @s ida.cd 0
$execute if entity @s[tag=ida.boss] run kill @e[tag=ida.target,scores={ida.sid=$(id)}]
