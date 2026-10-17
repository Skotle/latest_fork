execute if score #level inf.sys matches 3 run return 0
scoreboard players set #level inf.sys 3
scoreboard players add #epoch inf.sys 1
difficulty hard
tellraw @a {text:"[Infernal] HARD",color:"gold"}
function infernal:scan
