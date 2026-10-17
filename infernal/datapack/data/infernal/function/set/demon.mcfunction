execute if score #level inf.sys matches 6 run return 0
scoreboard players set #level inf.sys 6
scoreboard players add #epoch inf.sys 1
difficulty hard
tellraw @a {text:"[Infernal] DEMON",color:"gold"}
function infernal:scan
