$summon minecraft:spider ~ ~ ~ {"Tags":["ida.boss","ida.boss.kisegi_sanctuary","ida.newboss"],"CustomName":{"text":"키세기의 비단 여왕","color":"red"},"CustomNameVisible":1b,"PersistenceRequired":1b,"CanPickUpLoot":0b,"Health":$(hp)f,"attributes":[{"id":"minecraft:max_health","base":$(hp)},{"id":"minecraft:knockback_resistance","base":0.65},{"id":"minecraft:follow_range","base":48},{"id":"minecraft:scale","base":2.3},{"id":"minecraft:movement_speed","base":0.3},{"id":"minecraft:attack_damage","base":5}],"equipment":{},"drop_chances":{},"DeathLootTable":"dungeons_arise:boss/kisegi_sanctuary","data":{"id":$(id),"kind":"kisegi_sanctuary","name":"키세기의 비단 여왕","hp":$(hp),"color":"red","period":11,"primary":"web","secondary":"fangs"}}
execute as @e[tag=ida.newboss,distance=..2,limit=1,sort=nearest] at @s run function dungeons_arise:boss/core/setup with entity @s data
execute unless data entity @s data.anchored run function dungeons_arise:boss/site/anchor with entity @s data
scoreboard players set @s ida.stage 1
scoreboard players set @s ida.idle 0
scoreboard players set #spawned ida.tmp 1
tellraw @a[distance=..96] {"text":"[IDA] 키세기의 비단 여왕 출현! 노란 공격 표식을 피하세요.","color":"gold"}
playsound minecraft:entity.wither.spawn hostile @a[distance=..64] ~ ~ ~ 0.4 1.4
