#Summon the boss, fancily! First, trap the player and tag the marker for later.
execute if block ~ ~ ~ minecraft:trapped_chest[facing=north] run tag @s add North
execute if block ~ ~ ~ minecraft:trapped_chest[facing=south] run tag @s add South
execute if block ~ ~ ~ minecraft:trapped_chest[facing=east] run tag @s add East
execute if block ~ ~ ~ minecraft:trapped_chest[facing=west] run tag @s add West

execute if entity @s[tag=North] run fill ~10 ~5 ~-8 ~-10 ~-2 ~-8 infested_cobblestone replace air
execute if entity @s[tag=North] run fill ~10 ~5 ~9 ~-10 ~-2 ~9 infested_cobblestone replace air
execute if entity @s[tag=North] run fill ~-10 ~5 ~-8 ~-10 ~-2 ~9 infested_cobblestone replace air
execute if entity @s[tag=North] run fill ~10 ~5 ~-8 ~10 ~-2 ~9 infested_cobblestone replace air
execute if entity @s[tag=North] run fill ~-10 ~-2 ~-8 ~10 ~-2 ~9 infested_cobblestone replace air
execute if entity @s[tag=North] run fill ~-10 ~5 ~-8 ~10 ~5 ~9 infested_cobblestone replace air

execute if entity @s[tag=South] run fill ~10 ~5 ~8 ~-10 ~-2 ~8 infested_cobblestone replace air
execute if entity @s[tag=South] run fill ~10 ~5 ~-9 ~-10 ~-2 ~-9 infested_cobblestone replace air
execute if entity @s[tag=South] run fill ~-10 ~5 ~8 ~-10 ~-2 ~-9 infested_cobblestone replace air
execute if entity @s[tag=South] run fill ~10 ~5 ~8 ~10 ~-2 ~-9 infested_cobblestone replace air
execute if entity @s[tag=South] run fill ~-10 ~-2 ~8 ~10 ~-2 ~-9 infested_cobblestone replace air
execute if entity @s[tag=South] run fill ~-10 ~5 ~8 ~10 ~5 ~-9 infested_cobblestone replace air

execute if entity @s[tag=East] run fill ~8 ~5 ~10 ~8 ~-2 ~-10 infested_cobblestone replace air
execute if entity @s[tag=East] run fill ~-9 ~5 ~10 ~-9 ~-2 ~-10 infested_cobblestone replace air
execute if entity @s[tag=East] run fill ~8 ~5 ~-10 ~-9 ~-2 ~-10 infested_cobblestone replace air
execute if entity @s[tag=East] run fill ~8 ~5 ~10 ~-9 ~-2 ~10 infested_cobblestone replace air
execute if entity @s[tag=East] run fill ~8 ~-2 ~-10 ~-9 ~-2 ~10 infested_cobblestone replace air
execute if entity @s[tag=East] run fill ~8 ~5 ~-10 ~-9 ~5 ~10 infested_cobblestone replace air

execute if entity @s[tag=West] run fill ~-8 ~5 ~10 ~-8 ~-2 ~-10 infested_cobblestone replace air
execute if entity @s[tag=West] run fill ~9 ~5 ~10 ~9 ~-2 ~-10 infested_cobblestone replace air
execute if entity @s[tag=West] run fill ~-8 ~5 ~-10 ~9 ~-2 ~-10 infested_cobblestone replace air
execute if entity @s[tag=West] run fill ~-8 ~5 ~10 ~9 ~-2 ~10 infested_cobblestone replace air
execute if entity @s[tag=West] run fill ~-8 ~-2 ~-10 ~9 ~-2 ~10 infested_cobblestone replace air
execute if entity @s[tag=West] run fill ~-8 ~5 ~-10 ~9 ~5 ~10 infested_cobblestone replace air

execute if entity @s[tag=North] at @s run playsound witherstormmod:block_cluster_shake block @a ~ ~ ~-8
execute if entity @s[tag=South] at @s run playsound witherstormmod:block_cluster_shake block @a ~ ~ ~8
execute if entity @s[tag=East] at @s run playsound witherstormmod:block_cluster_shake block @a ~8 ~ ~
execute if entity @s[tag=West] at @s run playsound witherstormmod:block_cluster_shake block @a ~-8 ~ ~

setblock ~ ~ ~ air destroy
playsound minecraft:entity.zombie.break_wooden_door hostile @a ~ ~ ~ 1 1.25
playsound blue_skies:entity.arachnarch.screech hostile @a ~ ~ ~ 1 1.5

tag @s remove DragonsbaneSpawn
tag @s add DragonsbaneArena

summon twilightforest:pinch_beetle ~ ~ ~ {Tags:["DragonsbaneBoss","Phase1","DamageNerfed"],DeathLootTable:"explorers_eve:dragonsbane",PortalCooldown:100000,PersistenceRequired:1b,Motion:[0d,0.65d,0d],Health:200f,Attributes:[{Name:generic.max_health,Base:200},{Name:generic.follow_range,Base:64},{Name:generic.movement_speed,Base:0.3}],CustomNameVisible:0b,CustomName:'{"text":"드래곤베인"}',ArmorItems:[{id:"minecraft:leather_boots",Count:1b,tag:{Unbreakable:1b,Enchantments:[{id:"minecraft:fire_protection",lvl:10s},{id:"minecraft:feather_falling",lvl:10s},{id:"minecraft:blast_protection",lvl:10s},{id:"minecraft:projectile_protection",lvl:4s}]}},{},{},{}],ArmorDropChances:[0f,0f,0f,0f]}
execute as @e[tag=DragonsbaneBoss,limit=1,sort=nearest] store result score @s Health run data get entity @s Health
scoreboard players set @e[tag=DragonsbaneBoss,limit=1,sort=nearest] DragonsbaneLungeWait 100
scoreboard players set @e[tag=DragonsbaneBoss,limit=1,sort=nearest] DragonsbaneDigWait 200

#Give the boss infinite Remedy to prevent cheesing with Aether poison.
effect give @e[tag=DragonsbaneBoss,limit=1,sort=nearest] aether:remedy infinite 0 true

#Prepare a bossbar.
bossbar add dragonsbane "Dragonsbane"
bossbar set minecraft:dragonsbane color yellow
execute store result bossbar minecraft:dragonsbane max run scoreboard players get @e[tag=DragonsbaneBoss,limit=1,sort=nearest] Health
execute store result bossbar minecraft:dragonsbane value run scoreboard players get @e[tag=DragonsbaneBoss,limit=1,sort=nearest] Health

#Don't forget about other players!
tp @a[gamemode=!spectator,distance=8..32,predicate=explorers_eve:structure/jungle_temple] @p[gamemode=!spectator]

#And a marker!
summon marker ~ ~ ~ {Tags:["DragonsbaneTracker","Phase1"]}