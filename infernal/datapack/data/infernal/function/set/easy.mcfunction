execute if score #level inf.sys matches 1 run return 0
scoreboard players set #level inf.sys 1
scoreboard players add #epoch inf.sys 1
difficulty easy
tellraw @a {text:"[Infernal] EASY",color:"gold"}
function infernal:scan
