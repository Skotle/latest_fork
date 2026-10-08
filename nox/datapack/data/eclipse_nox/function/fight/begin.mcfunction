scoreboard players set #state nx.state 1
scoreboard players set #phase nx.phase 1
scoreboard players set #safe nx.safe 0
bossbar set eclipse_nox:health name {"text":"일식의 종지기, 녹스","color":"gold"}
scoreboard players set #time nx.time 0
scoreboard players set #cast nx.cast 0
scoreboard players set #skill nx.skill 0
scoreboard players set #idle nx.idle 0
scoreboard players set #grace nx.grace 300
scoreboard players set #next nx.next 80
scoreboard players set #step nx.step 0
scoreboard players set #lock nx.lock 0
scoreboard players set #last nx.last 0
scoreboard players set #puzzle nx.puzzle 0
scoreboard players set #max nx.max 450
execute as @a[tag=nox.member] run scoreboard players add #max nx.max 450
execute if score #max nx.max matches 1801.. run scoreboard players set #max nx.max 1800
scoreboard players add @a[tag=nox.member] nx.death 0
scoreboard players add @a[tag=nox.member] nx.leave 0
execute as @a[tag=nox.member] run scoreboard players operation @s nx.olddeath = @s nx.death
execute as @a[tag=nox.member] run scoreboard players operation @s nx.oldleave = @s nx.leave
execute store result storage eclipse_nox:runtime hp int 1 run scoreboard players get #max nx.max
function eclipse_nox:fight/summon with storage eclipse_nox:runtime
execute store result bossbar eclipse_nox:health max run scoreboard players get #max nx.max
bossbar set eclipse_nox:health players @a[tag=nox.member]
bossbar set eclipse_nox:health visible true
function eclipse_nox:arena/open
tellraw @a[tag=nox.member] {"text": "녹스: 첫 종이 울렸다. 과거의 발자국을 기억하라.", "color": "gold"}
playsound eclipse_nox:bell_low master @a[tag=nox.member] ~ ~ ~ 1 .6
scoreboard players set #dash nx.dash 0
scoreboard players set #expose nx.expose 0
scoreboard players set #cycle nx.combo 0
scoreboard players set #chain nx.combo 0
scoreboard players set #previous nx.anim -1
scoreboard players set #moving nx.move 0
scoreboard players set #oldhp nx.hp -1
scoreboard players set #next nx.next 20
scoreboard players set #adds nx.add 0
scoreboard players set #doom nx.doom 0
scoreboard players set #judgement nx.doom 0
function eclipse_nox:minions/spawn
scoreboard players set #counter nx.move 0
scoreboard players set #break nx.add 0
scoreboard players set @a[tag=nox.member] nx.clean 1
advancement grant @a[tag=nox.member] only eclipse_nox:challenge/root
scoreboard players set #team_acolyte nx.acolyte 0
scoreboard players set #team_adds nx.warden 0
scoreboard players set #window nx.window 0
scoreboard players set #mistakes nx.tmp 0
scoreboard players set #sealclean nx.tmp 0
execute store result score #party nx.tmp if entity @a[tag=nox.member]
execute as @a[tag=nox.member] run function eclipse_nox:challenge/reset_run
