execute if score #level inf.sys matches 4 run return 0
scoreboard players set #level inf.sys 4
scoreboard players add #epoch inf.sys 1
difficulty hard
tellraw @a {text:"[Infernal] HARDER",color:"gold"}
function infernal:scan
