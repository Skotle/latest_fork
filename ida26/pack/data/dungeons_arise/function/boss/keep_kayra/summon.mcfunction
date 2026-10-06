$summon minecraft:vindicator ~ ~ ~ {"Tags":["ida.boss","ida.boss.keep_kayra","ida.newboss"],"CustomName":{"text":"카이라의 늪지 기사","color":"red"},"CustomNameVisible":1b,"PersistenceRequired":1b,"CanPickUpLoot":0b,"Health":$(hp)f,"attributes":[{"id":"minecraft:max_health","base":$(hp)},{"id":"minecraft:knockback_resistance","base":0.65},{"id":"minecraft:follow_range","base":48},{"id":"minecraft:scale","base":1.15},{"id":"minecraft:movement_speed","base":0.3},{"id":"minecraft:attack_damage","base":7}],"equipment":{"mainhand":{"id":"minecraft:iron_axe","count":1},"head":{"id":"minecraft:iron_helmet","count":1,"components":{"minecraft:unbreakable":{}}},"chest":{"id":"minecraft:diamond_chestplate","count":1}},"drop_chances":{"mainhand":0.0,"head":0.0,"chest":0.0},"DeathLootTable":"dungeons_arise:boss/keep_kayra","data":{"id":$(id),"kind":"keep_kayra","name":"카이라의 늪지 기사","hp":$(hp),"color":"red","period":12,"primary":"cleave","secondary":"tide"}}
execute as @e[tag=ida.newboss,distance=..2,limit=1,sort=nearest] at @s run function dungeons_arise:boss/core/setup with entity @s data
execute unless data entity @s data.anchored run function dungeons_arise:boss/site/anchor with entity @s data
scoreboard players set @s ida.stage 1
scoreboard players set @s ida.idle 0
scoreboard players set #spawned ida.tmp 1
tellraw @a[distance=..96] {"text":"[IDA] 카이라의 늪지 기사 출현! 노란 공격 표식을 피하세요.","color":"gold"}
playsound minecraft:entity.wither.spawn hostile @a[distance=..64] ~ ~ ~ 0.4 1.4
