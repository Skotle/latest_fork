scoreboard objectives add fw.guard dummy
scoreboard objectives add fw.state dummy
scoreboard objectives add fw.time dummy
scoreboard objectives add fw.cast dummy
scoreboard objectives add fw.next dummy
scoreboard objectives add fw.skill dummy
scoreboard objectives add fw.cycle dummy
scoreboard objectives add fw.phase dummy
scoreboard objectives add fw.hp dummy
scoreboard objectives add fw.max dummy
scoreboard objectives add fw.tmp dummy
scoreboard objectives add fw.id dummy
scoreboard objectives add fw.age dummy
scoreboard objectives add fw.safe dummy
scoreboard objectives add fw.hits dummy
scoreboard objectives add fw.shield dummy
scoreboard objectives add fw.adds dummy
scoreboard objectives add fw.olddeath dummy
scoreboard objectives add fw.oldleave dummy
scoreboard objectives add fw.blink dummy
scoreboard objectives add fw.stun dummy
team add fw.enemies
team modify fw.enemies friendlyFire false
bossbar add frost_warden:health {text:"서리의 파수꾼",color:"aqua"}
bossbar set frost_warden:health color blue
scoreboard players set #state fw.state 0
execute unless score #serial fw.id matches 0.. run scoreboard players set #serial fw.id 0
function frost_warden:cleanup
