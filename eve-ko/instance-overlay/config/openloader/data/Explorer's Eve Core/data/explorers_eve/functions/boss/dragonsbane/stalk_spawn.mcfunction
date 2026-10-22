#Summon the boss, sneakily!
summon twilightforest:pinch_beetle ~ ~-0.9 ~ {Tags:["DragonsbaneBoss","Phase2","StalkSpawn","DragonsbaneDigging","DragonsbaneEmerge","DamageNerfed"],DeathLootTable:"explorers_eve:dragonsbane",PortalCooldown:100000,PersistenceRequired:1b,Motion:[0d,0.65d,0d],Health:200f,Attributes:[{Name:generic.max_health,Base:200},{Name:generic.follow_range,Base:64},{Name:generic.movement_speed,Base:0.3}],CustomNameVisible:0b,CustomName:'{"text":"드래곤베인"}',ArmorItems:[{id:"minecraft:leather_boots",Count:1b,tag:{Unbreakable:1b,Enchantments:[{id:"minecraft:fire_protection",lvl:10s},{id:"minecraft:feather_falling",lvl:10s},{id:"minecraft:blast_protection",lvl:10s},{id:"minecraft:projectile_protection",lvl:8s}]}},{},{},{}],ArmorDropChances:[0f,0f,0f,0f],Invulnerable:1b,NoAI:1b}

#Give the boss infinite Remedy to prevent cheesing with Aether poison.
effect give @e[tag=DragonsbaneBoss,limit=1,sort=nearest] aether:remedy infinite 0 true

#Prepare a bossbar, and set health to whatever it was before.
bossbar add dragonsbane "Dragonsbane"
bossbar set minecraft:dragonsbane color yellow
execute store result bossbar minecraft:dragonsbane max run data get entity @e[tag=DragonsbaneBoss,limit=1,sort=nearest] Health

execute unless score $DragonsbaneData Health matches 80.. run scoreboard players set $DragonsbaneData Health 80
execute store result entity @e[tag=DragonsbaneBoss,limit=1,sort=nearest] Health float 1 run scoreboard players get $DragonsbaneData Health
execute as @e[tag=DragonsbaneBoss,limit=1,sort=nearest] store result score @s Health run data get entity @s Health

execute store result bossbar minecraft:dragonsbane value run scoreboard players get @e[tag=DragonsbaneBoss,limit=1,sort=nearest] Health

#It spawns in the act of digging.
scoreboard players set @e[tag=DragonsbaneBoss,limit=1,sort=nearest] DragonsbaneDigTime 10
scoreboard players set @e[tag=DragonsbaneBoss,limit=1,sort=nearest] DragonsbaneDigWait 250
scoreboard players set @e[tag=DragonsbaneBoss,limit=1,sort=nearest] DragonsbaneMobWait 30
scoreboard players set @e[tag=DragonsbaneBoss,limit=1,sort=nearest] DragonsbaneLungeWait 150

#Effects!
playsound blue_skies:entity.arachnarch.charge hostile @a ~ ~ ~ 1 1.5
tag @p[gamemode=!spectator,tag=DragonsbaneStalking] remove DragonsbaneStalking

#And a marker!
summon marker ~ ~ ~ {Tags:["DragonsbaneTracker"]}