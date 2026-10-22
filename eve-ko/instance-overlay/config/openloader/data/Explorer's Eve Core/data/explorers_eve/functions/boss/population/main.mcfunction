#Main manager for Arachnarch AND Starlit Crusher changes.
execute unless entity @s[tag=Activated] run function explorers_eve:boss/population/activate

#Keep track of its health.
execute store result score @s Health run data get entity @s Health

#Phase transition.
execute if entity @s[tag=Phase1] if score @s Health < @s HealthLimit run function explorers_eve:boss/population/phase_2
execute if entity @s[tag=Phase2] if score @s Health > @s HealthLimit run function explorers_eve:boss/population/phase_1

#Ice Bombs are disappointing.
execute as @e[type=twilightforest:thrown_ice,distance=..48] at @s run function explorers_eve:item/ice_staff/melt_ice_bomb

#Starlit Crusher roots.
execute if entity @s[tag=SpawnRoots] if entity @e[type=blue_skies:ent_wall,distance=..5] unless entity @e[tag=StarlitRootMark,distance=..40] run scoreboard players remove @s StarlitRootTime 1
execute if entity @s[tag=SpawnRoots,scores={StarlitRootTime=..0}] run function explorers_eve:boss/population/root_start
execute if entity @e[tag=SpawnRoots] as @e[tag=StarlitRootMark,limit=1,sort=nearest,distance=..64] at @s run function explorers_eve:boss/population/root_timer

#Arachnarch spiders.
execute if entity @s[tag=SpawnSpiders] if entity @e[type=blue_skies:nested_spider,distance=..30] run function explorers_eve:boss/population/spiders

#Arachnarch Venom Spit nerf.
execute as @e[type=blue_skies:venom_spit,distance=..48,tag=!SpitChecked] run function explorers_eve:boss/population/spit_check
execute as @e[tag=VenomTracker,distance=..64] at @s unless entity @e[type=blue_skies:venom_bomb,distance=..2] run function explorers_eve:boss/population/spit_bomb

#Starlit Crusher hint.
execute if entity @s[type=blue_skies:starlit_crusher,tag=Phase1] if entity @e[type=blue_skies:ent_wall,distance=..8] unless entity @s[nbt={WallRegrowthTime:100}] run title @a[distance=..48] actionbar {"text":"Soulbound Spear를 사용하여 Starlit Crusher를 기절시키세요!","color":"light_purple"}

#Arachnarch hint.
execute if entity @s[type=blue_skies:arachnarch,tag=Phase1] if entity @s[nbt={Charging:1b}] run title @a[distance=..24] actionbar {"text":"스파이크 쉴드를 사용하여 아라크나크를 기절시키세요!","color":"light_purple"}