$bossbar remove dungeons_arise:encounter_$(id)
$bossbar add dungeons_arise:encounter_$(id) {"text":"$(name)","color":"gold"}
$bossbar set dungeons_arise:encounter_$(id) max $(hp)
$bossbar set dungeons_arise:encounter_$(id) color $(color)
$bossbar set dungeons_arise:encounter_$(id) style notched_10
$bossbar set dungeons_arise:encounter_$(id) players @a[predicate=dungeons_arise:boss/eligible,distance=..96]
