execute if score #level inf.sys matches 7 run return 0
scoreboard players set #level inf.sys 7
scoreboard players add #epoch inf.sys 1
difficulty hard
tellraw @a {text:"[Infernal] NIGHTMARE",color:"gold"}
function infernal:scan
