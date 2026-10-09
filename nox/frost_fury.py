"""v22: faster Ashe rotation, >=2.5x arrow coefficients, selective projectile protection penetration."""
import copy,json,zipfile
from build import BASE,DP,OUT,js
from frost import fn,call,append,N
from frost_ashe import edit

def generate():
 edit('skills/begin',lambda s:s.replace('#cast fw.cast 36','#cast fw.cast 26').replace('#cast fw.cast 48','#cast fw.cast 32').replace('#cast fw.cast 28','#cast fw.cast 20').replace('matches 2 run scoreboard players set #cast fw.cast 32','matches 2 run scoreboard players set #cast fw.cast 24').replace('#next fw.next 32','#next fw.next 8').replace('#next fw.next 24','#next fw.next 6').replace('#next fw.next 20','#next fw.next 4').replace('약한 화살 5발 연사','강화 화살 5발 연사').replace('발사 후 긴 반격 기회','발사 후 짧은 반격 기회'))
 edit('skills/casting',lambda s:s.replace('matches 28 at','matches 18 at').replace('matches 22 at','matches 15 at').replace('matches 10 at','matches 9 at').replace('matches 4 at','matches 6 at').replace('matches 16 at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ facing entity @a[tag=fw.active,gamemode=!creative,sort=nearest,limit=1] eyes','matches 12 at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ facing entity @a[tag=fw.active,gamemode=!creative,sort=nearest,limit=1] eyes'))
 edit('skills/recover',lambda s:s.replace('#safe fw.safe 30','#safe fw.safe 10').replace('#safe fw.safe 20','#safe fw.safe 6').replace('#safe fw.safe 50','#safe fw.safe 24'))
 edit('arrows/normal',lambda s:s.replace('value 1.6d','value 4.0d'))
 edit('arrows/adopt',lambda s:s.replace('damage:1.6d','damage:4.0d'))
 edit('arrows/add_adopt',lambda s:s.replace('damage:1.0d','damage:2.5d'))
 edit('ashe/focus_shot',lambda s:s.replace('value .9d','value 2.4d'))
 edit('arrows/stun',lambda s:s.replace('damage:2.5d','damage:6.5d'))
 # Native skeleton shots can collide before adoption on their first tick.
 edit('fight/carrier',lambda s:s.replace('"minecraft:enchantments":{}','"minecraft:enchantments":{"minecraft:power":5}'))
 # Preserve vanilla registry metadata and requirements; only change the EPF contribution
 # for projectile damage sourced by this faction. Never modify a player's equipment.
 with zipfile.ZipFile(BASE/'engine-test/versions/26.3/server-26.3.jar') as z:
  protection=json.loads(z.read('data/minecraft/enchantment/projectile_protection.json'))
 original=protection['effects']['minecraft:damage_protection'][0]
 faction={'type':'minecraft:damage_source_properties','predicate':{'source_entity':{'minecraft:nbt':'{Tags:["fw.owned"]}'}}}
 normal=copy.deepcopy(original)
 normal['requirements']={'type':'minecraft:all_of','terms':[original['requirements'],{'type':'minecraft:inverted','term':faction}]}
 weakened=copy.deepcopy(original)
 weakened['requirements']={'type':'minecraft:all_of','terms':[original['requirements'],faction]}
 weakened['effect']['value']['base']=1.0
 weakened['effect']['value']['per_level_above_first']=1.0
 protection['effects']['minecraft:damage_protection']=[normal,weakened]
 js(DP/'data/minecraft/enchantment/projectile_protection.json',protection)
 guide=json.loads((OUT/'Frost-guide.json').read_text(encoding='utf-8'))
 guide.update(revision=22,recovery_ticks=[6,10,24],cooldown_ticks_by_phase=[8,6,4])
 guide['passive']['ordinary_arrow_damage_base']=4.0
 guide['focus'].update(spacing_ticks=3,damage_base=2.4,warning_ticks=6)
 guide['volley']['warning_ticks']=10
 guide['ultimate'].update(damage_base=6.5,warning_ticks=16,recovery_ticks=24)
 guide['wall_volley']['warning_ticks']=10
 guide['arrow_damage_multipliers']={'ordinary':2.5,'focus':2.4/.9,'ultimate':6.5/2.5,'adds':2.5}
 guide['projectile_protection']={'scope':'Projectile damage sourced by fw.owned boss/add faction only','epf_per_level_before':2,'epf_per_level_after':1,'penetration':.5,'other_protection_unchanged':True,'equipment_never_rewritten':True,'vanilla_total_epf_cap':20,'example_single_IV':{'reduction_before':.32,'reduction_after':.16},'example_four_IV':{'reduction_before':.8,'reduction_after':.64},'semantics':'Halves the contribution before vanilla EPF cap; does not halve the final capped total armor reduction.'}
 js(OUT/'Frost-guide.json',guide)
