#Timer until recovery.
scoreboard players remove @s InjuryDelay 1
playsound witherstormmod:command_block_summon hostile @a[distance=..200] ~ ~ ~ 5 1.5 1

execute store result score @s Health run data get entity @s Health
execute if score @s Health < @s HealthLimit run function explorers_eve:final/wound
execute if entity @s[tag=FinalBossVulnerable] run title @a[tag=FinalBattling] actionbar {"text":"위더 스톰은 취약합니다! 공격!","color":"light_purple"}

#Generate an amount of mobs to spawn, then loop the spawn function until they're done.
scoreboard players set @s RandomRange 6
function explorers_eve:random
scoreboard players operation @s CommandEntityCount = @s RandomValue
scoreboard players add @s CommandEntityCount 2
execute unless score @s InjuryDelay matches 7.. if score @s CommandEntityCount matches 1.. positioned ~ ~10 ~ run function explorers_eve:final/mob_spawn

#If the Storm's HP is below certain thresholds, drop the delay and move on.
execute if entity @s[tag=Phase1,scores={Health=..400}] unless data storage world FinalBossCheckpoint2 run scoreboard players set @s InjuryDelay 0
execute if entity @s[tag=Phase1,scores={Health=..250}] if data storage world FinalBossCheckpoint2 unless data storage world FinalBossCheckpoint3 run scoreboard players set @s InjuryDelay 0
execute if entity @s[tag=Phase1,scores={Health=..150}] if data storage world FinalBossCheckpoint3 run scoreboard players set @s InjuryDelay 0
execute if entity @s[tag=Phase3,scores={Health=..250}] run scoreboard players set @s InjuryDelay 0
execute if entity @s[tag=Phase5,scores={Health=..150}] run scoreboard players set @s InjuryDelay 0

execute if score @s InjuryDelay matches ..0 if entity @s[tag=PhaseTransition] run function explorers_eve:final/phase_transition
execute if score @s InjuryDelay matches ..0 unless entity @s[tag=PhaseTransition] if entity @a[tag=FinalBattling,tag=!FinalBattleDied,distance=..256] run function explorers_eve:final/injury_end