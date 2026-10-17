execute if score #level inf.sys matches 0 run return 0
scoreboard players set #level inf.sys 0
scoreboard players add #epoch inf.sys 1
difficulty peaceful
tellraw @a {text:"[Infernal] PEACEFUL",color:"gold"}
function infernal:scan
