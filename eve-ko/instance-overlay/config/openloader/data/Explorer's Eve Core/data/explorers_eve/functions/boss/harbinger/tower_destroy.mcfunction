#Remove the tower.
setblock ~ ~ ~ air
kill @e[tag=EMPCrystal,limit=1,sort=nearest,distance=..10]
fill ~-1 ~-1 ~-1 ~1 ~6 ~1 air destroy
summon minecraft:creeper ~ ~ ~ {Tags:["ApocalypseIgnore"],Fuse:0,ExplosionRadius:4b,CustomName:'{"text":"EMP 타워"}'}

forceload remove ~ ~ ~ ~

kill @s