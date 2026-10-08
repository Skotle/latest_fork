summon minecraft:item_display ~ ~ ~ {Tags:["db.capture"],view_range:0f}
item replace entity @e[tag=db.capture,limit=1] contents from entity @s hotbar.7
data modify storage desert_ball:capture stack set from entity @e[tag=db.capture,limit=1] item
data modify storage desert_ball:capture stack.count set value 1
data modify storage desert_ball:capture uuid set from entity @s UUID
execute store result storage desert_ball:ctx owner int 1 run scoreboard players get @s db.owner
function desert_ball:theft/save with storage desert_ball:ctx
item modify entity @s hotbar.7 desert_ball:take_one
scoreboard players set @s db.debt 1
scoreboard players set #captured db.tmp 1
kill @e[tag=db.capture]
tellraw @s {text:"아이템 1개 도난! 보스나 준비 공을 맞히면 반환됩니다. 무기·방어구는 보호됩니다.",color:"red"}
