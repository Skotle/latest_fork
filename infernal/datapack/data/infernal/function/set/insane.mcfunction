execute if score #level inf.sys matches 5 run return 0
scoreboard players set #level inf.sys 5
scoreboard players add #epoch inf.sys 1
difficulty hard
tellraw @a {text:"[Infernal] INSANE",color:"gold"}
function infernal:scan
