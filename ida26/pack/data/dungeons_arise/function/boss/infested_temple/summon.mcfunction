$summon minecraft:stray ~ ~ ~ {"Tags":["ida.boss","ida.boss.infested_temple","ida.newboss"],"CustomName":{"text":"서리 역병의 사제","color":"blue"},"CustomNameVisible":1b,"PersistenceRequired":1b,"CanPickUpLoot":0b,"Health":$(hp)f,"attributes":[{"id":"minecraft:max_health","base":$(hp)},{"id":"minecraft:knockback_resistance","base":0.65},{"id":"minecraft:follow_range","base":48},{"id":"minecraft:scale","base":1.15},{"id":"minecraft:movement_speed","base":0.3}],"equipment":{"mainhand":{"id":"minecraft:bow","count":1},"head":{"id":"minecraft:iron_helmet","count":1,"components":{"minecraft:unbreakable":{}}},"chest":{"id":"minecraft:diamond_chestplate","count":1}},"drop_chances":{"mainhand":0.0,"head":0.0,"chest":0.0},"DeathLootTable":"dungeons_arise:boss/infested_temple","data":{"id":$(id),"kind":"infested_temple","name":"서리 역병의 사제","hp":$(hp),"color":"blue","period":11,"primary":"frost","secondary":"plague"}}
execute as @e[tag=ida.newboss,distance=..2,limit=1,sort=nearest] at @s run function dungeons_arise:boss/core/setup with entity @s data
execute unless data entity @s data.anchored run function dungeons_arise:boss/site/anchor with entity @s data
scoreboard players set @s ida.stage 1
scoreboard players set @s ida.idle 0
scoreboard players set #spawned ida.tmp 1
tellraw @a[distance=..96] {"text":"[IDA] 서리 역병의 사제 출현! 노란 공격 표식을 피하세요.","color":"gold"}
playsound minecraft:entity.wither.spawn hostile @a[distance=..64] ~ ~ ~ 0.4 1.4
