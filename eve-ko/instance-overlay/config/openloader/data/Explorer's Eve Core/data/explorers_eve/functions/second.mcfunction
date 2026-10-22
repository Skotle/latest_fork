#This stuff isn't as essential to update as what's in the tick file, so they're run 1/20th as often to keep lag away.
#Run this function every second.
schedule function explorers_eve:second 1s

#Secondary initializer. Only ever runs once per player.
execute as @a unless entity @s[tag=Loaded] run function explorers_eve:load/player

#If the player is out of the Twilight Forest too early, shove them back. This has to happen before Wither Storm checks to prevent an obscure bug involving teleporting...
execute as @a[tag=TwilightStuck,predicate=!explorers_eve:twilight_forest] in twilightforest:twilight_forest run function explorers_eve:load/player_twilight

#Activate any new Wither Storm.
execute as @w[tag=!FinalBoss,tag=!Activated] at @s run function explorers_eve:storm/activate

#Rather than checking the Storm's NBT data over and over (bad practice), use a scoreboard and check that instead.
execute as @e[type=witherstormmod:wither_storm,tag=!FinalBoss] store result score @s StormPhase run witherstormmod phase get @s

#Run Storm checks every second.
execute as @e[scores={StormPhase=4..},tag=!CommandBlockHurt] at @s if entity @s[nbt={PlayDeadManager:{State:0}}] run function explorers_eve:storm/main

#Injure the Storm's heads if it's playing dead.
execute as @w[tag=BombLit,tag=!PlayDeadInjured] at @s if entity @e[type=witherstormmod:command_block,distance=..100] run function explorers_eve:storm/phase_6_injure

#If the progression-essential bomb goes off, the Wither Storm will always get exploded.
execute as @w[tag=BombLit,tag=!PlayDeadInjured] at @s unless entity @e[type=witherstormmod:formidibomb,distance=..500] run witherstormmod explode @s

#Revive the Wither Storm if the player flees.
execute as @e[type=witherstormmod:command_block] at @s unless dimension witherstormmod:bowels unless entity @a[gamemode=!spectator,distance=..250] as @w[nbt={PlayDeadManager:{State:2}},distance=..100] run function explorers_eve:storm/revive

#If the Wither Storm's Command Block has been hurt and it can't attack, keep checking for beam effects anyway.
execute as @w[tag=CommandBlockHurt] at @s as @a[gamemode=!spectator,distance=..200] at @s at @e[type=#explorers_eve:wither_storm_part,distance=..200] run function explorers_eve:storm/beam/check

#If the Wither Storm's Command Block is nearly broken, scatter clusters as if it's falling apart.
execute as @w[tag=CommandBlockInjury3] at @s if entity @a[gamemode=!spectator,distance=..200] positioned ~ ~50 ~ run function explorers_eve:storm/injury/single_cluster

#Final battle effects.
execute as @w[tag=FinalBoss] at @s run function explorers_eve:final/main

#Final battle player effects.
execute as @a[tag=FinalBattling] at @s unless predicate explorers_eve:overworld unless predicate explorers_eve:glitch run function explorers_eve:final/player/unmark

#Final battle item effects.
execute as @e[tag=FinalBossStar] at @s unless entity @a[gamemode=!spectator,distance=..8] run function explorers_eve:final/item_particles

#Sickened mobs spawned by the Wither Storm can't despawn unless it's gone.
execute as @e[tag=StormSpawned] at @s unless entity @w[distance=..250] run function explorers_eve:storm/mobs_despawn

#Tracks if the Symbiont is alive, and if not, what happens next.
execute as @e[tag=SymbiontTracker] at @s run function explorers_eve:symbiont/track

#Check if a Formidibomb exists, and if so, make it make particles.
execute as @e[type=witherstormmod:formidibomb,tag=!FormidibombParticlesStart] at @s run function explorers_eve:item/formidibomb/particles_start

#Players atop Dark Leaves suffer.
execute as @a[gamemode=!spectator] at @s if block ~ ~-1 ~ twilightforest:hardened_dark_leaves run function explorers_eve:world/darkwood_leaves_effects

#Players in a snowy temple get mining fatigue until they reach the top. DEBUG, no they don't.
#execute as @a[gamemode=!spectator] at @s if predicate explorers_eve:structure/snowy_temple if entity @e[tag=SnowyTempleMark,distance=..80] run function explorers_eve:world/mining_fatigue

#Similar with jungle temple. DEBUG, nope.
#execute as @a[gamemode=!spectator] at @s if predicate explorers_eve:structure/jungle_temple if entity @e[tag=DragonsbaneSpawn,distance=..128] run function explorers_eve:world/mining_fatigue

#Players in an ocean monument get mining fatigue immediately if any Elder Guardians are around.
execute as @a[gamemode=!spectator] at @s if predicate explorers_eve:structure/ocean_monument if entity @e[type=minecraft:elder_guardian,distance=..64] run function explorers_eve:world/mining_fatigue

#Check for players trying to make/update a tainted gem.
execute as @a[predicate=explorers_eve:tainted_gem] at @s if block ~1 ~ ~1 witherstormmod:tainted_dust if block ~1 ~ ~ witherstormmod:tainted_dust if block ~1 ~ ~-1 witherstormmod:tainted_dust if block ~ ~ ~1 witherstormmod:tainted_dust if block ~ ~ ~-1 witherstormmod:tainted_dust if block ~-1 ~ ~1 witherstormmod:tainted_dust if block ~-1 ~ ~ witherstormmod:tainted_dust if block ~-1 ~ ~-1 witherstormmod:tainted_dust run function explorers_eve:item/tainted_gem/check

#If the dragon exists, mark that and manage it.
execute as @e[type=ender_dragon] at @s unless entity @e[tag=DragonTracker,distance=0..] run summon marker 0 100 0 {Tags:["DragonTracker"]}

#Any new End Crystals are marked.
execute as @e[type=end_crystal,tag=!CrystalMarked] run function explorers_eve:world/end_crystal_mark
execute as @e[type=end_crystal,tag=CrystalTimer] run function explorers_eve:world/end_crystal_timer

#Check armor stands, and if it's the one on the plateau castle, add the Ignis arena. This is split into two functions to make sure the arena spawns before killing the marker.
execute as @e[type=armor_stand,tag=!ArmorStandChecked] run function explorers_eve:world/plateau_castle_check
execute as @e[tag=IgnisArena] at @s run function explorers_eve:world/plateau_castle_set

#Prevent Wither from overhealing without a player nearby.
execute as @e[type=wither,tag=Phase2] at @s unless entity @a[gamemode=!spectator,distance=..80] run function explorers_eve:boss/wither/health_fix

#Naga fight changes.
execute as @e[type=twilightforest:naga] at @s run function explorers_eve:boss/naga/main

#Lich initialization.
execute as @e[type=twilightforest:lich] unless entity @s[tag=LichChecked] run function explorers_eve:boss/lich/check

#Minoshroom fight changes.
execute as @e[type=twilightforest:minoshroom] at @s if entity @a[gamemode=!spectator,distance=..40] run function explorers_eve:boss/minoshroom/main

#Knight Phantom spawner timer.
scoreboard players add @e[tag=PhantomSpawnerMark] PhantomTime 1
execute as @e[tag=PhantomSpawnerMark,scores={PhantomTime=6..}] at @s run function explorers_eve:boss/knight_phantom/spawner_break

#Prevent the Hydra from overhealing in phase 3.
execute as @e[type=twilightforest:hydra,tag=!FinalBattle,tag=Phase3] at @s unless entity @a[gamemode=!spectator,distance=..32] run function explorers_eve:boss/hydra/health_fix

#When the Hydra dies, clear out the arena.
execute as @e[tag=HydraTracker] at @s unless entity @e[type=twilightforest:hydra,distance=..30,scores={Health=1..}] run function explorers_eve:boss/hydra/death

#Activates when the Ur-Ghast dies.
execute as @e[tag=UrGhastTracker] at @s unless entity @e[type=twilightforest:ur_ghast,distance=..128] run function explorers_eve:boss/ur_ghast/death

#Alpha Yeti fight changes.
execute as @e[type=twilightforest:alpha_yeti] at @s if entity @a[gamemode=!spectator,distance=..60] run function explorers_eve:boss/alpha_yeti/main

#Snow Queen fight changes.
execute as @e[type=twilightforest:snow_queen] at @s if entity @a[gamemode=!spectator,distance=..30] run function explorers_eve:boss/snow_queen/main

#When the Snow Queen dies, dispose of her arena trackers.
execute as @e[tag=IceArenaCenter] at @s unless entity @e[type=twilightforest:snow_queen,distance=..60] run function explorers_eve:boss/snow_queen/death

#Knight Phantom fight changes.
execute as @e[type=twilightforest:knight_phantom] at @s if entity @a[gamemode=!spectator,distance=..40] run function explorers_eve:boss/knight_phantom/main

#Track the Jungle Temple treasure room for Dragonsbane.
execute as @e[tag=DragonsbaneSpawn] at @s if entity @a[gamemode=!spectator,distance=..7.5] run function explorers_eve:boss/dragonsbane/spawn

#Track players stalked by Dragonsbane.
execute as @a[tag=DragonsbaneStalking,gamemode=!spectator] run function explorers_eve:boss/dragonsbane/stalk_timer

#Dragonsbane death effects.
execute as @e[tag=DragonsbaneTracker] at @s unless entity @e[tag=DragonsbaneBoss,distance=..128] run function explorers_eve:boss/dragonsbane/death

#When the Monstrosity dies, react.
execute as @e[tag=MonstrosityTracker,limit=1] at @s unless entity @e[type=cataclysm:netherite_monstrosity,distance=..80] run function explorers_eve:boss/netherite_monstrosity/death

#Track the unbuilt Netherite Monstrosity.
execute as @e[tag=MonstrosityGolem] at @s run function explorers_eve:boss/netherite_monstrosity/golem_wait

#The Ender Guardian's crystal despawns when the boss dies.
execute as @e[tag=VoidSpikeSource] at @s unless entity @e[type=cataclysm:ender_guardian,distance=..128] run function explorers_eve:boss/ender_guardian/death

#Ignis's arena breaks when the fight's over.
execute as @e[tag=IgnisTracker] at @s unless entity @e[type=cataclysm:ignis,distance=..80] run function explorers_eve:boss/ignis/death

#Prevent Harbinger from overhealing.
execute as @e[type=cataclysm:the_harbinger] at @s unless entity @a[gamemode=!spectator,distance=..64] run function explorers_eve:boss/harbinger/health_fix

#When the Harbinger dies, clear out the arena.
execute as @e[tag=HarbingerTracker] at @s unless entity @e[type=cataclysm:the_harbinger,distance=..256] run function explorers_eve:boss/harbinger/death

#Nameless Sorcerer death effects.
execute as @e[tag=SorcererTracker] at @s unless entity @e[tag=SorcererBoss,distance=..128] run function explorers_eve:boss/sorcerer/death

#Blinding boss changes.
execute as @e[type=#explorers_eve:blinding_boss,tag=!FinalBattle] at @s if entity @a[gamemode=!spectator,distance=..24] run function explorers_eve:boss/blinding/main

#Blinding boss death cleanup.
execute as @e[tag=BlindingTracker] at @s unless entity @e[type=#explorers_eve:blinding_boss,distance=..24] run function explorers_eve:boss/blinding/death

#Slider death effects.
execute as @e[tag=SliderMarkRoot] at @s unless entity @e[type=aether:slider,distance=..40] run function explorers_eve:boss/slider/death

#Valkyrie Queen death effects.
execute as @e[tag=ValkyrieQueenTracker] at @s unless entity @e[type=aether:valkyrie_queen,distance=..80] run function explorers_eve:boss/valkyrie_queen/death

#Sun Spirit death effects.
execute as @e[tag=SunSpiritTracker] at @s unless entity @e[type=aether:sun_spirit,distance=..30] run function explorers_eve:boss/sun_spirit/death

#Wandering Trader upgrades.
execute as @e[type=minecraft:wandering_trader,tag=!TraderUpgraded] at @s run function explorers_eve:world/wandering_trader_check

#If there's a player in the bowels, the Command Block battle activates.
execute as @e[type=witherstormmod:command_block] at @s if dimension witherstormmod:bowels run function explorers_eve:command_block/main

#If there's a player in the bowels, upgrade the mobs.
execute as @a[gamemode=!spectator,predicate=explorers_eve:bowels] at @s as @e[type=#witherstormmod:sickened_mobs,distance=..64,tag=!BowelsMob] at @s run function explorers_eve:command_block/mobs/main

#Buffed Sickened Parrots power up nearby mobs. This particle function calls the effects function when it concludes.
execute as @e[tag=SupportParrot] at @s positioned ~ ~0.25 ~ as @e[type=#witherstormmod:sickened_mobs,tag=!SupportParrot,distance=..12] facing entity @s eyes run function explorers_eve:command_block/mobs/parrot_buff_particles

#Corpses in the Aether fall out.
execute as @e[type=corpse:corpse] at @s if dimension aether:the_aether positioned ~ 1 ~ unless entity @s[dy=999999] in minecraft:overworld run tp @s ~ 319 ~

#Corpses in the End make particles.
execute as @e[type=corpse:corpse,tag=EndCorpse] at @s run particle minecraft:end_rod ~ ~24 ~ 0.25 8 0.25 0.05 20 force @a[distance=..128]

#Always check to see if Super TNT should be absorbed by the Wither Storm.
execute as @e[type=witherstormmod:super_tnt,tag=!PlayDeadOverride] unless entity @w[nbt={PlayDeadManager:{State:0}}] run tag @s add PlayDeadOverride
execute as @e[type=witherstormmod:super_tnt,tag=!PlayDeadOverride] at @s run function explorers_eve:item/super_tnt/check

#Check if Super TNT exists near a Wither Storm, and if so, wait for it to explode.
execute as @e[type=witherstormmod:super_tnt,tag=!DistractionChecked,tag=!PlayDeadOverride] unless data storage world DraconicTemperament at @s if entity @w[scores={StormPhase=4..},distance=..350] run function explorers_eve:item/super_tnt/mark

#Check if the Formidibomb is near a phase 6+ Wither Storm, and if so, funny things happen.
execute as @e[type=witherstormmod:formidibomb,tag=!AngerFocus] at @s if entity @w[scores={StormPhase=6..},distance=..250] run function explorers_eve:item/formidibomb/anger_mark

#If the player's not in the bowels, update their tag.
execute as @e[type=witherstormmod:command_block] run tag @a[predicate=!explorers_eve:bowels] remove CommandBattling

#Blue Skies mobs are rarely endermen.
execute as @e[type=#explorers_eve:blue_skies_hostile,tag=!EndermanChecked] at @s run function explorers_eve:world/blue_skies/enderman_tag

#Check zombies and slow down babies.
execute as @e[type=#explorers_eve:can_be_baby,tag=!BabyChecked] run function explorers_eve:world/baby_zombie_slowness

#Check drowned, and if they're in a Warped Garden, they become pain.
execute as @e[type=minecraft:drowned,tag=!DrownedChecked] at @s run function explorers_eve:world/drowned_trident_check

#Some mobs can't drop their gear.
execute as @e[type=#explorers_eve:prevent_gear_drops,tag=!NoDrops] run function explorers_eve:world/prevent_drops

#Some mobs don't do as much damage.
execute as @e[type=#explorers_eve:nerf_attack_damage,tag=!DamageNerfed] at @s run function explorers_eve:world/nerf_attack_damage

#Friendly Artificial Golems are better.
execute as @e[type=blue_skies:artificial_golem,tag=!GolemBuffed] at @s run function explorers_eve:world/artificial_golem_check

#Vex ally targets injure vexes, and when allies slay their target, they die.
execute as @e[tag=AllyVexTarget] at @s run function explorers_eve:item/vexation_totem/target_scan
execute as @e[tag=AllyVex] at @s unless entity @e[tag=AllyVexTarget,distance=..128] run function explorers_eve:item/vexation_totem/vex_scan

#Tick down custom item cooldowns.
execute as @a[tag=VexationUsed] run function explorers_eve:item/vexation_totem/cooldown
execute as @a[tag=IceStaffUsed] run function explorers_eve:item/ice_staff/cooldown
execute as @a[tag=LichScepterUsed] run function explorers_eve:item/lich_scepter/cooldown

#Iron Bubble buff.
execute as @a[curios={item:{id:"aether:iron_bubble"}}] run function explorers_eve:item/iron_bubble
execute as @a[curios={item:{id:"aether:iron_bubble",tag:{display:{Lore:['{"italic":false,"color":"gray","text":"물 속에 있는 동안 호흡, 시야, 속도, 가속을 부여합니다."}','{"color":"gold","text":"탐험가의 보물"}']}}}}] run function explorers_eve:item/iron_bubble

execute as @a[tag=IronBubble,predicate=!explorers_eve:conduit_power] run function explorers_eve:item/iron_bubble_end

#If a player's died, detect that.
execute as @a[scores={Deaths=1..}] at @s run function explorers_eve:world/player_death

#If a player's died recently, let them keep their mercy tag for a while.
execute as @a[tag=RecentDeath] at @s run function explorers_eve:world/player_death_timer

#Reload if the player asks for it.
execute as @a[scores={Reload=1..}] run function explorers_eve:load/reset

#Hide command feedback when the player holds a guidebook to prevent trigger text from appearing.
execute unless data storage world GuideHeld if entity @a[gamemode=!spectator,predicate=explorers_eve:guidebook] run function explorers_eve:item/guide/hold
execute if data storage world GuideHeld unless entity @a[gamemode=!spectator,predicate=explorers_eve:guidebook] run function explorers_eve:item/guide/unhold

#Main music checkers.
execute as @a[tag=!MusicPlaying] at @s run function explorers_eve:music/check_player
execute as @a[tag=!NullMusic,tag=!ResummonMusic] at @s run function explorers_eve:music/check_null