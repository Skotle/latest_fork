#Need unique functions for the intros because they change so much at once.
playsound explorers_eve:glitch_theme_intro record @s ~ ~ ~ 1 1 1
scoreboard players set @s MusicTime 831
tag @s add GlitchIntro
tellraw @s [{"text":"지금 재생 중:","color":"gray","italic":true},{"text":"모든 결함의 아버지","italic":true,"underlined":true},{"text":", 퀼버 제작","italic":true}]