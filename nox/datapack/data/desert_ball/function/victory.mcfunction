tellraw @a[tag=db.member] {"text": "사막의 볼을 꺾었다! 도난품을 반환합니다.", "color": "gold"}
execute as @a[tag=db.active] run give @s minecraft:golden_boots[minecraft:item_name={text:"크리스티아누의 황금 축구화",color:"gold"}]
function desert_ball:abort
