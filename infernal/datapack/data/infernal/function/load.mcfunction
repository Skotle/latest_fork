scoreboard objectives add inf.sys dummy
scoreboard objectives add inf.rev dummy
scoreboard objectives add inf.id dummy
execute unless score #level inf.sys matches 0..7 run function infernal:init
tellraw @a {text:"[Infernal] /function infernal:menu",color:"gold"}
