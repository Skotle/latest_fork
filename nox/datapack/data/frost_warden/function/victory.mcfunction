execute as @a[tag=fw.active,gamemode=!creative] run function frost_warden:reward
tellraw @a[tag=fw.member] {"text": "서리의 파수꾼을 쓰러뜨렸습니다!", "color": "aqua"}
function frost_warden:abort
