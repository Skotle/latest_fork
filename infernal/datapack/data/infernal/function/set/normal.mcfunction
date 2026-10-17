execute if score #level inf.sys matches 2 run return 0
scoreboard players set #level inf.sys 2
scoreboard players add #epoch inf.sys 1
difficulty normal
tellraw @a {text:"[Infernal] NORMAL",color:"gold"}
function infernal:scan
