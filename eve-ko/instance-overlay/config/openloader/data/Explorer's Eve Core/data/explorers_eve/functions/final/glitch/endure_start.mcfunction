#The block becomes immune and begins the final countdown.
kill @e[tag=CommandRide]
summon rabbit ~ ~ ~ {Silent:1b,Invulnerable:1b,NoGravity:1b,Tags:["CommandRide"],DeathLootTable:"minecraft:empty",PortalCooldown:1000000,ActiveEffects:[{Id:14,Amplifier:0b,Duration:1000000,ShowParticles:0b}],Health:600f,Attributes:[{Name:generic.movement_speed,Base:0.1},{Name:generic.max_health,Base:600},{Name:generic.follow_range,Base:200}]}
data modify entity @s BossfightManager.CurrentPhase set value 5
data modify entity @s State set value 0
tag @s remove GlitchHurt
tag @s add GlitchEndure
tag @s add ShortImmune
tag @w[tag=FinalBoss] remove Phase10
tag @w[tag=FinalBoss] add Phase11
scoreboard players reset @s GlitchHurtTime
scoreboard players set @s GlitchAttackTime 0
scoreboard players set @s GlitchHitsPossible 9
scoreboard players set @s GlitchShortTime 999999
scoreboard players set @s GlitchEndureTime 600

#Cleanup minions.
tp @e[tag=FinalBattle,predicate=explorers_eve:glitch] ~ -1000 ~
kill @e[tag=FinalBattle,predicate=explorers_eve:glitch]
kill @e[tag=GlitchBossChoice]
kill @e[tag=GlitchBossTracker]

#Chat!
tellraw @a[predicate=explorers_eve:glitch] [{"text":"< 명령 블록 >"},{"text":"심각한 손상이 감지되었습니다! 수리를 위해 자원을 전환하는 중..."}]