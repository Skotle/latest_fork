#Hold the block in place and make effects.
summon block_display ~ ~ ~ {billboard:"center",Tags:["GlitchTransportDisplay"],brightness:{sky:15,block:15},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[-0.5f,-0.5f,-0.5f],scale:[1f,1f,1f]},block_state:{Name:"minecraft:command_block",Properties:{facing:"south"}}}

playsound minecraft:block.portal.trigger hostile @a[tag=FinalBattling] ~ ~ ~ 10 2 1
playsound minecraft:block.portal.trigger hostile @a[tag=FinalBattleDied] ~ ~ ~ 10 2 1

summon bat ~ ~ ~ {Silent:1b,Invulnerable:1b,Tags:["SparkBat"],ActiveEffects:[{Id:14,Amplifier:0b,Duration:1000000,ShowParticles:0b}],Attributes:[{Name:generic.movement_speed,Base:3}]}
summon bat ~ ~ ~ {Silent:1b,Invulnerable:1b,Tags:["SparkBat"],ActiveEffects:[{Id:14,Amplifier:0b,Duration:1000000,ShowParticles:0b}],Attributes:[{Name:generic.movement_speed,Base:3.5}]}
summon bat ~ ~ ~ {Silent:1b,Invulnerable:1b,Tags:["SparkBat"],ActiveEffects:[{Id:14,Amplifier:0b,Duration:1000000,ShowParticles:0b}],Attributes:[{Name:generic.movement_speed,Base:4}]}
scoreboard players set @e[tag=SparkBat,limit=3,sort=nearest] GlitchSparkTime 59

#Dispose of mobs.
kill @e[type=#witherstormmod:sickened_mobs,distance=..500]

#Revive dead players.
execute as @a[tag=FinalBattleDied] at @a[gamemode=!spectator,gamemode=!creative,limit=1,sort=nearest] run function explorers_eve:final/player/respawn

#And give a fun chat message!
tellraw @a[tag=FinalBattling] [{"text":"< 명령 블록 >"},{"text":"차원 시뮬레이션 구성 중..."}]
execute if data storage world GlitchGenerated run tellraw @a[tag=FinalBattling] [{"text":"< 명령 블록 >"},{"text":"기존 시뮬레이션이 발견되었습니다! 다시 초기화하는 중..."}]
data modify storage world GlitchGenerated set value 1