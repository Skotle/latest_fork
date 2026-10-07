scoreboard objectives add nx.anim dummy
scoreboard objectives add nx.move dummy
scoreboard objectives add nx.dash dummy
scoreboard objectives add nx.total dummy
scoreboard objectives add nx.expose dummy
scoreboard objectives add nx.recover dummy
scoreboard objectives add nx.combo dummy
scoreboard objectives add nx.state dummy
scoreboard objectives add nx.time dummy
scoreboard objectives add nx.phase dummy
scoreboard objectives add nx.hp dummy
scoreboard objectives add nx.max dummy
scoreboard objectives add nx.skill dummy
scoreboard objectives add nx.cast dummy
scoreboard objectives add nx.idle dummy
scoreboard objectives add nx.step dummy
scoreboard objectives add nx.last dummy
scoreboard objectives add nx.lock dummy
scoreboard objectives add nx.puzzle dummy
scoreboard objectives add nx.safe dummy
scoreboard objectives add nx.angle dummy
scoreboard objectives add nx.olddeath dummy
scoreboard objectives add nx.oldleave dummy
scoreboard objectives add nx.tmp dummy
scoreboard objectives add nx.next dummy
scoreboard objectives add nx.grace dummy
scoreboard objectives add nx.dx dummy
scoreboard objectives add nx.dz dummy
scoreboard objectives add nx.forward dummy
scoreboard objectives add nx.side dummy
scoreboard objectives add nx.death deathCount
scoreboard objectives add nx.leave minecraft.custom:minecraft.leave_game
bossbar add eclipse_nox:health {"text":"일식의 종지기, 녹스","color":"gold"}
bossbar set eclipse_nox:health color purple
bossbar set eclipse_nox:health style notched_20
execute unless score #state nx.state matches 0.. run scoreboard players set #state nx.state 0
execute unless score #installed nx.state matches 0.. run scoreboard players set #installed nx.state 0
execute if score #state nx.state matches 1 run function eclipse_nox:admin/abort
tellraw @a {"text":"[녹스 v2] 관측소가 새 오버월드 청크의 지하에 생성됩니다. /locate structure eclipse_nox:observatory","color":"gray"}
scoreboard objectives add nx.add dummy
scoreboard objectives add nx.doom dummy
scoreboard objectives add nx.mx dummy
scoreboard objectives add nx.mz dummy
scoreboard objectives add nx.mid dummy
