tellraw @s [{"text":"Silent Storm 챌린지가 활성화되었습니다.","color":"light_purple"}]
data modify storage world SilentStorm set value 1
scoreboard players set @s Challenge -1

execute as @e[type=#explorers_eve:wither_storm_part] run data modify entity @s Silent set value 1b
witherstormmod config server set server.misc.smartBossbar true