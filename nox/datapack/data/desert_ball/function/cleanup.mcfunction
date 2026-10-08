scoreboard players set #pending db.tmp 0
kill @e[tag=db.boss]
kill @e[tag=db.visual]
kill @e[tag=db.core]
kill @e[tag=db.shot]
kill @e[tag=db.fall]
kill @e[tag=db.ambush]
kill @e[tag=db.jump_origin]
bossbar set desert_ball:health visible false
tag @e[tag=db.current] remove db.current
tag @a remove db.member
tag @a remove db.active
scoreboard players set #cast db.cast 0
