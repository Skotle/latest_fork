scoreboard players set #phase fw.phase 2
function frost_warden:adds/spawn
tellraw @a[tag=fw.member] {"text": "서리 화살 강화! 짧은 둔화를 경계하고 기둥을 이용하세요.", "color": "aqua"}
