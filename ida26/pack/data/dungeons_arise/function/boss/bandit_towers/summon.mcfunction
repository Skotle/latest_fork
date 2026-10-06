$summon minecraft:pillager ~ ~ ~ {"Tags":["ida.boss","ida.boss.bandit_towers","ida.newboss"],"CustomName":{"text":"붉은 절벽의 저격수","color":"red"},"CustomNameVisible":1b,"PersistenceRequired":1b,"CanPickUpLoot":0b,"Health":$(hp)f,"attributes":[{"id":"minecraft:max_health","base":$(hp)},{"id":"minecraft:knockback_resistance","base":0.65},{"id":"minecraft:follow_range","base":48},{"id":"minecraft:scale","base":1.15},{"id":"minecraft:movement_speed","base":0.3}],"equipment":{"mainhand":{"id":"minecraft:crossbow","count":1},"head":{"id":"minecraft:iron_helmet","count":1,"components":{"minecraft:unbreakable":{}}}},"drop_chances":{"mainhand":0.0,"head":0.0},"DeathLootTable":"dungeons_arise:boss/bandit_towers","data":{"id":$(id),"kind":"bandit_towers","name":"붉은 절벽의 저격수","hp":$(hp),"color":"red","period":10,"primary":"snipe","secondary":"reinforcements"}}
execute as @e[tag=ida.newboss,distance=..2,limit=1,sort=nearest] at @s run function dungeons_arise:boss/core/setup with entity @s data
execute unless data entity @s data.anchored run function dungeons_arise:boss/site/anchor with entity @s data
scoreboard players set @s ida.stage 1
scoreboard players set @s ida.idle 0
scoreboard players set #spawned ida.tmp 1
tellraw @a[distance=..96] {"text":"[IDA] 붉은 절벽의 저격수 출현! 노란 공격 표식을 피하세요.","color":"gold"}
playsound minecraft:entity.wither.spawn hostile @a[distance=..64] ~ ~ ~ 0.4 1.4
