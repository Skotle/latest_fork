tellraw @s [{"text":"용의 기질 도전이 비활성화되었습니다.","color":"light_purple"}]
data remove storage world DraconicTemperament
scoreboard players set @s Challenge -1

witherstormmod config server set server.targeting.tractorPullSpeedModifier 0.3
witherstormmod config server set server.targeting.headEscapeTime 40
witherstormmod config server set server.targeting.specialTargetingBiasChance 60

#execute as @e[type=witherstormmod:wither_storm] run attribute @s witherstormmod:slow_flying_speed modifier remove 823a104f-3438-12ab-b968-cc41ce8930d7