#Tick down the timer until the phase ends.
particle end_rod ~ ~ ~ 0.35 0.35 0.35 0.3 2 force
function explorers_eve:final/glitch/color_cycle

execute as @e[tag=CommandRide,limit=1,sort=nearest] at @s facing entity @p[gamemode=!spectator] eyes rotated ~ 0 run tp @s ^ ^ ^0.5

execute if entity @a[gamemode=!spectator,distance=0..8] run data modify entity @e[tag=CommandRide,limit=1,sort=nearest] Motion[1] set value 0.6d
execute if entity @a[gamemode=!spectator,distance=8..20] run data modify entity @e[tag=CommandRide,limit=1,sort=nearest] Motion[1] set value 0.45d
execute if entity @a[gamemode=!spectator,distance=20..32] run data modify entity @e[tag=CommandRide,limit=1,sort=nearest] Motion[1] set value 0.3d
execute unless entity @a[gamemode=!spectator,distance=0..32] unless block ~ ~-40 ~ air run data modify entity @e[tag=CommandRide,limit=1,sort=nearest] Motion[1] set value 0d
execute unless entity @a[gamemode=!spectator,distance=0..32] if block ~ ~-40 ~ air run data modify entity @e[tag=CommandRide,limit=1,sort=nearest] Motion[1] set value -1d

#Steadily kill monsters, and constantly get rid of unneeded clusters.
kill @e[type=#witherstormmod:sickened_mobs,predicate=explorers_eve:glitch,limit=1,sort=random]

#As time goes by, decrease the Wither Storm's health to make a timer that lasts until the end of the phase.
execute if score @s GlitchEndureTime matches 5.. store result entity @w[tag=FinalBoss] Health float 0.84 run scoreboard players get @s GlitchEndureTime

#Messages!
execute if score @s GlitchEndureTime matches 500 run tellraw @a[predicate=explorers_eve:glitch] [{"text":"< 명령 블록 >"},{"text":"오류 503!","color":"red"},{"text":"프로그램 virtual_dimension.cmd를 재정의하는 중..."}]
execute if score @s GlitchEndureTime matches 400 run tellraw @a[predicate=explorers_eve:glitch] [{"text":"< 명령 블록 >"},{"text":"시스템 리소스가 부족합니다! virtual_dimension.cmd 프로그램을 지원할 수 없습니다..."}]
execute if score @s GlitchEndureTime matches 300 run tag @e[tag=FinalBoss] add ForceScatter
execute if score @s GlitchEndureTime matches 200 run tellraw @a[predicate=explorers_eve:glitch] [{"text":"< 명령 블록 >"},{"text":"강제 시스템 재설정 중..."}]

scoreboard players remove @s GlitchAttackTime 1
execute if score @s GlitchAttackTime matches ..0 run function explorers_eve:final/glitch/attack/endure/choose

scoreboard players remove @s GlitchEndureTime 1
execute if score @s GlitchEndureTime matches ..0 run function explorers_eve:final/glitch/escape