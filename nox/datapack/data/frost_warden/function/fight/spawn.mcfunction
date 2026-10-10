scoreboard players set #state fw.state 1
scoreboard players set #time fw.time 0
scoreboard players set #idle fw.tmp 0
scoreboard players set #cast fw.cast 0
scoreboard players set #safe fw.safe 0
scoreboard players set #next fw.next 36
scoreboard players set #cycle fw.cycle 0
scoreboard players set #phase fw.phase 1
scoreboard players set #max fw.max 450
execute as @a[tag=fw.member] run scoreboard players add #max fw.max 450
execute if score #max fw.max matches 1801.. run scoreboard players set #max fw.max 1800
execute store result storage frost_warden:ctx hp int 1 run scoreboard players get #max fw.max
function frost_warden:fight/carrier with storage frost_warden:ctx
scoreboard players operation #pool fw.hp = #max fw.max
scoreboard players set #hundred fw.tmp 100
scoreboard players operation #pool fw.hp *= #hundred fw.tmp
scoreboard players set #last fw.hp 100000
execute as @a[tag=fw.member] run scoreboard players add @s nx.death 0
execute as @a[tag=fw.member] run scoreboard players add @s nx.leave 0
execute as @a[tag=fw.member] run scoreboard players operation @s fw.olddeath = @s nx.death
execute as @a[tag=fw.member] run scoreboard players operation @s fw.oldleave = @s nx.leave
scoreboard players set @a[tag=fw.member] fw.hits 0
scoreboard players set @a[tag=fw.member] fw.shield 0
scoreboard players set #adds fw.adds 0
execute as @a[tag=fw.member] run advancement grant @s only frost_warden:root
bossbar set frost_warden:health players @a[tag=fw.member]
bossbar set frost_warden:health visible true
tellraw @a[tag=fw.member] {"text": "서리의 파수꾼! 폭발 화살·머리 위 폭격 — 표식을 보고 이동하고 장전 중 반격하세요.", "color": "aqua"}
scoreboard players set #blink fw.blink 200
scoreboard players set #enraged fw.tmp 0
function frost_warden:teleport/setup
function frost_warden:walls/setup
scoreboard players set #focus fw.tmp 0
scoreboard players set #wall_side fw.tmp 0
scoreboard players set @a[tag=fw.member] fw.guard 0
scoreboard players set #walk fw.walk 0
scoreboard players set #steps fw.walk 0
scoreboard players set #blink fw.blink 120
