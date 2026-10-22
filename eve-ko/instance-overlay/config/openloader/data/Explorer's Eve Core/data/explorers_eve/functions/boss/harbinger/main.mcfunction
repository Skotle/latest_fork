#Main manager for Harbinger changes. Include an extra command to run on the second tick to force target a player.
execute if entity @s[tag=Activated,tag=!Aggro] run function explorers_eve:boss/harbinger/aggro
execute unless entity @s[tag=Activated] run function explorers_eve:boss/harbinger/activate

#Keep track of its health. Don't let it heal, ever.
function explorers_eve:boss/harbinger/health_fix

#At the start of the fight, no EMP spikes!
execute if entity @s[tag=EMPDeny] run function explorers_eve:boss/harbinger/emp_deny

#Tick down the delay for EMP spikes to drop.
execute unless entity @e[tag=HarbingerTowerMark,distance=..128] run scoreboard players remove @s HarbingerTowerTime 1
execute if score @s Health matches ..100 unless entity @s[tag=FinalTowersUsed] unless entity @e[tag=HarbingerTowerMark,distance=..128] run scoreboard players set @s HarbingerTowerTime -1
execute if score @s HarbingerTowerTime matches ..-1 run function explorers_eve:boss/harbinger/tower_start

#Towers do stuff.
execute as @e[tag=HarbingerTowerMark,distance=..256] at @s run function explorers_eve:boss/harbinger/tower_track

#If the player is withered, change that.
execute as @a[predicate=explorers_eve:wither_2,distance=..64] run function explorers_eve:boss/harbinger/wither_effect

#Give hints.
execute if entity @e[type=cataclysm:death_laser_beam,distance=..4] unless entity @s[tag=FinalBattle] run title @a[distance=..40] actionbar {"text":"레이저로부터 살아남기 위해 블록 뒤에 숨어보세요!","color":"light_purple"}
execute if entity @e[tag=TowerActive,tag=!TowerOverload,distance=..64] unless entity @s[tag=FinalBattle] run title @a[distance=..40] actionbar {"text":"수정을 파괴하여 타워의 총격을 막으세요!","color":"light_purple"}
execute if entity @e[tag=TowerOverload,tag=!TowerUsed,distance=..64] unless entity @s[tag=FinalBattle] run title @a[distance=..40] actionbar {"text":"Harbinger를 타워로 유인하고 버튼을 눌러 기절시키세요!","color":"light_purple"}

#Keep the marker here.
tp @e[tag=HarbingerTracker,limit=1,sort=nearest,distance=..128] @s