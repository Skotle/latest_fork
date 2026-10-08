scoreboard players add @s nx.wins 1
execute if score #team_acolyte nx.acolyte matches 0 run advancement grant @s only eclipse_nox:challenge/no_acolyte
execute if score #team_adds nx.warden matches 0 run advancement grant @s only eclipse_nox:challenge/no_adds
execute if score @s nx.wins matches 3.. run advancement grant @s only eclipse_nox:challenge/veteran
execute if score #party nx.tmp matches 1 run advancement grant @s only eclipse_nox:challenge/solo
execute if score #time nx.time matches ..3600 run advancement grant @s only eclipse_nox:challenge/speed
execute if score #sealclean nx.tmp matches 1 run advancement grant @s only eclipse_nox:challenge/pure_seal
execute if score @s nx.trials matches 3.. run advancement grant @s only eclipse_nox:challenge/trials
execute if score @s nx.counter matches 3.. run advancement grant @s only eclipse_nox:challenge/counter_master
