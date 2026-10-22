#Set up some important things.
scoreboard players set @s StormAttackWait 1000
function explorers_eve:storm/teleport/set_cap
advancement revoke @a only explorers_eve:super_tnt
advancement revoke @a only explorers_eve:command_parts
advancement revoke @a only explorers_eve:command_parts_single
witherstormmod config server set server.flaming_skulls.flamingSkullExplosionSize default
witherstormmod consumedEntities lock @s
execute if entity @s[nbt={Phase:0}] run tag @s add Phase4ChasePrep
execute if entity @s[tag=Phase4ChasePrep] run scoreboard players set @s WitherBreak 400
execute if entity @s[tag=Phase4ChasePrep] run witherstormmod config server set server.flaming_skulls.flamingSkullExplosionSize 2.0
execute if entity @s[tag=Phase4ChasePrep] run effect give @e[type=#explorers_eve:twilight_passive,distance=..64] invisibility 5 0 true
execute if entity @s[tag=Phase4ChasePrep] run tp @e[type=#explorers_eve:twilight_passive,distance=..64] ~ -1000 ~
data modify storage world WitherStormSpawned set value 1
advancement grant @a only explorers_eve:wither_storm_exists
advancement grant @a only witherstormmod:main/root
execute if entity @w[tag=Activated] run tellraw @a {"text":"경고! 여러 개의 위더 스톰을 동시에 소환하면 예상치 못한 동작이 발생하므로 지원되지 않습니다.","color":"red"}
tag @s add Activated
tag @s add MobsSpawned
team join NoInfighting @s
execute if entity @s[nbt={Resummoned:1b}] run tag @s add Resummoned
execute unless entity @s[tag=Resummoned] run tag @s add FirstTeleport
execute if entity @s[tag=Resummoned] run advancement grant @a[distance=..500] only witherstormmod:main/resummon_wither_storm
execute if entity @s[tag=Resummoned] run attribute @s minecraft:generic.attack_damage modifier add 1533d04f-3438-43ab-b968-ab31de8133d7 StormDamage 8 add
execute if entity @s[tag=Resummoned] run data modify entity @s PlayDeadManager.RecentlyRevived set value 0b
execute if entity @s[tag=Resummoned] run witherstormmod config server set server.misc.rotationSpeed 0.3
execute if entity @s[tag=Resummoned] run witherstormmod ultimateTarget chase begin @s

#Lastly, make sure it's not somewhere silly.
execute if predicate explorers_eve:invalid_teleport in minecraft:overworld run tp @e[type=#explorers_eve:wither_storm_part] 0 400 0