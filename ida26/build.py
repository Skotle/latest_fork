import collections, gzip, hashlib, json, re, sys, zipfile
from pathlib import Path
from nbt_io import Tag, read, write

BASE=Path(__file__).resolve().parent
SRC=BASE/'original'; OUT=BASE/'pack'; RELEASE=BASE/'output'
stats=collections.Counter(); replacements={}
ITEMS={
 'builders_tea':'honey_bottle','goggles':'leather_helmet','brass_hand':'gold_ingot',
 'rose_quartz':'amethyst_shard','raw_zinc':'raw_iron','powdered_obsidian':'obsidian',
 'torch_arrow':'spectral_arrow','goblet':'glass_bottle','hourglass':'clock','statue':'armor_stand',
 'rope':'string','flute':'goat_horn','pickarang':'iron_pickaxe','andesite_alloy':'iron_ingot',
 'moss_paste':'moss_block','soap':'slime_ball','experience_nugget':'experience_bottle',
 'seed_pouch':'bundle','zinc_nugget':'iron_nugget','ash':'gunpowder','copper_nugget':'copper_nugget',
 'trowel':'iron_shovel','onion':'potato','straw_bale':'hay_block','potato_crate':'potato',
 'beetroot_crate':'beetroot','carrot_crate':'carrot','straw':'wheat','minced_beef':'beef',
 'bacon':'porkchop','ham':'cooked_porkchop','bomb':'tnt','forgotten_hat':'leather_helmet',
 'sweet_berry_cookie':'cookie','cake_slice':'cake','apple_pie_slice':'pumpkin_pie',
 'honeyed_apple':'golden_apple','crafting_blueprint':'paper','sack':'bundle','antique_ink':'ink_sac',
 'clear_shard':'glass','abacus':'comparator','quiver':'bundle','glow_lichen_growth':'glow_lichen',
 'wild_flax':'wheat_seeds','slime_in_a_bucket':'slime_ball','electron_tube':'redstone',
 'propeller':'iron_ingot','polished_rose_quartz':'amethyst_shard','cogwheel':'iron_nugget',
 'large_cogwheel':'iron_ingot','dirty_shard':'flint','wheat_flour':'wheat','dough':'bread',
 'bomb_blue':'tnt','super_glue':'slime_ball','wrench':'iron_pickaxe','crushed_raw_iron':'raw_iron',
 'crushed_raw_gold':'raw_gold','flint_knife':'iron_sword','rotten_tomato':'rotten_flesh',
 'soul_bead':'ender_pearl','mechanical_piston':'piston','sticky_mechanical_piston':'sticky_piston',
 'clipboard':'paper','whisk':'iron_ingot','experience_block':'experience_bottle',
 'tree_fertilizer':'bone_meal','fire_pit':'campfire',
}
BIOMES={
 'regular_forests':['forest','birch_forest','old_growth_birch_forest','dappled_forest'],
 'taigas':['taiga','old_growth_pine_taiga','old_growth_spruce_taiga'],
 'plains':['plains','sunflower_plains'],'dark_oak_forests':['dark_forest'],
 'savannas':['savanna','savanna_plateau','windswept_savanna'],
 'badlands':['badlands','eroded_badlands','wooded_badlands'],'deserts':['desert'],
 'nether_crimson_forests':['crimson_forest'],'nether_warped_forests':['warped_forest'],
 'nether_wastes':['nether_wastes'],'nether_souls':['soul_sand_valley'],
 'end_voids':['the_end','end_highlands','end_midlands','end_barrens','small_end_islands'],
 'meadows':['meadow'],'snowy_forests':['snowy_taiga','grove'],
 'snowy_mountains':['snowy_slopes','frozen_peaks','jagged_peaks'],
 'snowy_plains':['snowy_plains','ice_spikes'],'swamps':['swamp','mangrove_swamp'],
 'hills':['windswept_hills','windswept_forest','windswept_gravelly_hills'],
 'flower_forests':['flower_forest'],'floral':['flower_forest','meadow','cherry_grove'],
 'oceans':['ocean','deep_ocean','cold_ocean','deep_cold_ocean','frozen_ocean',
           'deep_frozen_ocean','lukewarm_ocean','deep_lukewarm_ocean','warm_ocean'],
}
def save(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def replace_item(s):
 if s.startswith('minecraft:'): return {'minecraft:chain':'minecraft:iron_chain'}.get(s,s)
 name=s.split(':')[-1]
 out='minecraft:'+('candle' if name.startswith('candle_holder') else ITEMS.get(name,'iron_ingot'))
 replacements[s]=out;stats['mod_item_replacements']+=1;return out
def predicate(x):
 if isinstance(x,list):return {'type':'minecraft:all_of','terms':[predicate(v) for v in x]}
 if not isinstance(x,dict):return x
 x=dict(x)
 if 'condition' in x: x['type']=x.pop('condition')
 if x.get('type')=='minecraft:entity_properties':x['predicate']=entity_predicate(x.get('predicate',{}))
 for key in ['terms','term']:
  if key in x:x[key]=[predicate(v) for v in x[key]] if isinstance(x[key],list) else predicate(x[key])
 return x
def entity_predicate(x):
 # Since 1.21.5 entity sub-predicates use their registry names.
 sub={'location','stepping_on','movement','effects','equipment','flags','slots','team','periodic_tick','type_specific','distance'}
 return {('minecraft:entity_type' if k=='type' else 'minecraft:'+k if k in sub else k):('#minecraft:sensitive_to_bane_of_arthropods' if v=='#minecraft:arthropod' else v) for k,v in x.items()}
def general(x):
 if isinstance(x,list):return [general(v) for v in x]
 if not isinstance(x,dict):return x
 x={k:general(v) for k,v in x.items()}
 if x.get('type') in {'item','loot_table','tag','empty','group','sequence','alternatives','uniform','binomial','constant'}:x['type']='minecraft:'+x['type']
 if 'Name' in x:x['id']=x.pop('Name')
 if 'Properties' in x:x['properties']=x.pop('Properties')
 if 'function' in x and isinstance(x['function'],str) and (x['function'].startswith('minecraft:') or ':' not in x['function']):
  t=x.pop('function');x['type']=t if ':' in t else 'minecraft:'+t
 if 'condition' in x and isinstance(x['condition'],str) and (x['condition'].startswith('minecraft:') or ':' not in x['condition']):
  t=x.pop('condition');x['type']=t if ':' in t else 'minecraft:'+t
 if 'conditions' in x and ('trigger' not in x):x['condition']=predicate(x.pop('conditions'))
 if 'functions' in x and x.get('type')!='minecraft:sequence':x['modifier']=x.pop('functions')
 if x.get('type')=='minecraft:entity_properties':x['predicate']=entity_predicate(x.get('predicate',{}))
 if 'requirements' in x and isinstance(x['requirements'],list) and x['requirements'] and isinstance(x['requirements'][0],dict):x['requirements']=predicate(x['requirements'])
 if 'minecraft:custom_model_data' in x and isinstance(x['minecraft:custom_model_data'],(int,float)):
  # The provided resource pack has no IDA models. Keep identifiers without selecting unrelated RP models.
  x['minecraft:custom_model_data']={'floats':[float(x['minecraft:custom_model_data'])]}
 if x.get('type')=='minecraft:item':x['name']=replace_item(x['name'])
 if x.get('type')=='minecraft:tag' and 'name' in x:x['items']='#'+x.pop('name').lstrip('#')
 if x.get('type')=='minecraft:match_tool':
  if 'items' in x.get('predicate',{}):
   val=x['predicate']['items'];x['predicate']['items']=[replace_item(v) for v in val] if isinstance(val,list) else replace_item(val)
 if x.get('type')=='minecraft:loot_table' and 'name' in x:x['value']=x.pop('name')
 if x.get('type')=='minecraft:set_enchantments':x.setdefault('add',False)
 for key in ['count','damage','levels','rolls','bonus_rolls','chance']:
  v=x.get(key)
  if isinstance(v,dict) and set(v)<= {'min','max'} and v:v['type']='minecraft:uniform'
 return x
def spawner_processor(p):
 ref=p['integrated_api_spawner_resourcelocation'].split(':')[1]
 mobs=json.loads((SRC/f'data/dungeons_arise/integrated_structure_spawners/{ref}.json').read_text())['mobs']
 mobs=[m for m in mobs if m['name'].startswith('minecraft:')]
 if not mobs:mobs=[{'name':'minecraft:zombie','weight':1}]
 data={'id':'minecraft:mob_spawner','SpawnData':{'entity':{'id':mobs[0]['name']},'custom_spawn_rules':{'block_light_limit':p['valid_block_light_level']}},
       'SpawnPotentials':[{'weight':m['weight'],'data':{'entity':{'id':m['name']},'custom_spawn_rules':{'block_light_limit':p['valid_block_light_level']}}} for m in mobs]}
 for a,b in {'delay':'Delay','max_nearby_entities':'MaxNearbyEntities','max_spawn_delay':'MaxSpawnDelay','min_spawn_delay':'MinSpawnDelay','required_player_range':'RequiredPlayerRange','spawn_count':'SpawnCount','spawn_range':'SpawnRange'}.items():data[b]=p[a]
 return {'processor_type':'minecraft:rule','rules':[{'input_predicate':{'predicate_type':'minecraft:block_match','block':'minecraft:spawner'},'location_predicate':{'predicate_type':'minecraft:always_true'},'output_state':{'id':'minecraft:spawner'},'block_entity_modifier':{'type':'minecraft:append_static','data':data}}]}
def process_json(rel,obj):
 s=rel.as_posix()
 if '/worldgen/structure/' in s and '/tags/' not in s:
  keep={'start_pool','size','max_distance_from_center','biomes','step','terrain_adaptation','project_start_to_heightmap','start_height','spawn_overrides','use_expansion_hack','liquid_settings'}
  obj={k:v for k,v in obj.items() if k in keep};obj['type']='minecraft:jigsaw';obj.setdefault('terrain_adaptation','none');obj.setdefault('use_expansion_hack',False);stats['structures']+=1
  obj['max_distance_from_center']=min(obj['max_distance_from_center'],116 if obj['terrain_adaptation']!='none' else 128)
  for override in obj['spawn_overrides'].values():
   for spawn in override['spawns']:
    low=spawn.pop('minCount');high=spawn.pop('maxCount');spawn['count']=low if low==high else {'type':'minecraft:uniform','min_inclusive':low,'max_inclusive':high}
 if '/worldgen/structure_set/' in s and '/tags/' not in s:
  obj['placement']['type']='minecraft:random_spread';obj['placement'].pop('super_exclusion_zone',None)
 if '/worldgen/template_pool/' in s:
  def pool(x):
   if isinstance(x,dict):
    if x.get('element_type','').startswith('integrated_api:'):
     for k in list(x):
      if k not in {'element_type','location','processors','projection'}:del x[k]
     x['element_type']='minecraft:single_pool_element'
    for v in x.values():pool(v)
   elif isinstance(x,list):
    for v in x:pool(v)
  pool(obj)
  valid=[]
  for entry in obj['elements']:
   e=entry['element'];loc=e.get('location','')
   if isinstance(loc,str) and loc.startswith('dungeons_arise:') and not (SRC/f"data/dungeons_arise/structure/{loc.split(':')[1]}.nbt").exists():
    stats['missing_template_entries_removed']+=1;continue
   valid.append(entry)
  obj['elements']=valid or [{'weight':1,'element':{'element_type':'minecraft:empty_pool_element'}}]
 if '/worldgen/processor_list/' in s:
  ps=[]
  for p in obj['processors']:
   t=p['processor_type']
   if t=='integrated_api:spawner_randomizing_processor':ps.append(spawner_processor(p));stats['spawner_processors']+=1
   elif t.startswith('minecraft:'):
    if t=='minecraft:rule':p['rules']=[rule for rule in p['rules'] if not any(isinstance(rule.get(k,{}).get('block'),str) and not rule[k]['block'].startswith('minecraft:') for k in ['input_predicate','location_predicate'])]
    ps.append(p)
   else:stats['removed_mod_processors']+=1
  obj['processors']=ps
 if '/tags/' in s:
  vals=[]
  for v in obj.get('values',[]):
   ident=v if isinstance(v,str) else v['id']
   if ident=='minecraft:potion':
    vals.extend(['minecraft:splash_potion','minecraft:lingering_potion']);continue
   if ident.startswith('#integrated_api:collections/'):
    vals.extend('minecraft:'+b for b in BIOMES[ident.split('/')[-1]])
   elif ident.lstrip('#').startswith(('minecraft:','dungeons_arise:')):vals.append(v)
   else:stats['removed_mod_tag_entries']+=1
  obj['values']=vals
 obj=general(obj)
 if '/advancement/' in s:
  icon=obj.get('display',{}).get('icon',{})
  if isinstance(icon,dict) and 'id' in icon:icon['id']=replace_item(icon['id'])
  for crit in obj['criteria'].values():
   if 'player' in crit.get('conditions',{}):crit['conditions']['player']=predicate(crit['conditions']['player'])
 return obj

BLOCK_EXACT={'copycat':'stone_bricks','copycat_step':'stone_brick_slab','copycat_panel':'stone_brick_slab','fluid_pipe':'iron_bars',
 'encased_fluid_pipe':'iron_block','fluid_tank':'glass','book_pile':'bookshelf','book_pile_horizontal':'bookshelf',
 'notice_board':'oak_sign','urn':'decorated_pot','goblet':'flower_pot','fire_pit':'campfire','monster_box':'spawner',
 'glass_frame':'glass','paper_wall':'white_stained_glass','timber_frame':'stripped_oak_wood','timber_cross_brace':'stripped_oak_wood',
 'rope_knot':'oak_fence','rope':'iron_chain','chute':'hopper','pulley_block':'oak_log','statue':'chiseled_stone_bricks',
 'pedestal':'quartz_pillar','planter':'flower_pot','flower_box':'flower_pot','end_stone_lamp':'sea_lantern',
 'table_cloth':'white_carpet','blackstone_tile':'polished_blackstone','bison_carpet':'gray_carpet','bison_fur_block':'gray_wool'}
def block_id(old):
 if old.startswith('minecraft:'):return old
 n=old.split(':')[1]
 if n in BLOCK_EXACT:new=BLOCK_EXACT[n]
 elif 'chest' in n:new='chest'
 elif 'shingle' in n:new=('deepslate_tile' if 'black' in n else 'brick')+('_stairs' if n.endswith('stairs') else '_slab' if n.endswith('slab') else 's')
 elif n.endswith('_stairs'):new='purpur_stairs' if old.startswith('betterend:') else 'stone_brick_stairs'
 elif n.endswith('_slab'):new='purpur_slab' if old.startswith('betterend:') else 'stone_brick_slab'
 elif n.endswith('_wall'):new='stone_brick_wall'
 elif 'ladder' in n:new='ladder'
 elif 'candle_holder' in n:new='candle'
 elif n.endswith('_fence_gate'):new='oak_fence_gate'
 elif n.endswith('_fence') or n.endswith('_post'):new='oak_fence'
 elif n.endswith('_door'):new='oak_door'
 elif n.endswith('_trapdoor'):new='oak_trapdoor'
 elif 'glass' in n:new='glass'
 elif 'leaves' in n:new='oak_leaves'
 elif any(v in n for v in ['plank','wood','log','bearing']):new='oak_planks'
 elif any(v in n for v in ['flower','hibiscus','mushroom']):new='red_tulip'
 elif 'sand' in n:new='sand'
 else:new='stone_bricks'
 new='minecraft:'+new;replacements[old]=new;stats['mod_palette_states']+=1;return new
def clean_nbt(d,context=''):
 # Drop mod capabilities/attachments, not vanilla custom loot/table data.
 for k in list(d):
  if k in ['ForgeCaps','ForgeData','neoforge:attachments'] or (':' in k and not k.startswith('minecraft:')):del d[k];continue
  t=d[k]
  if k=='final_state' and t.kind==8:
   ident=t.value.split('[')[0]
   if ':' in ident and not ident.startswith('minecraft:'):t.value=block_id(ident)
  if t.kind==8 and t.value=='clayworks:base':t.value='minecraft:base'
  if k=='sherds' and t.kind==9 and t.value[0]==8:t.value=(8,['minecraft:brick' if v=='minecraft:air' else v for v in t.value[1]])
  if k=='id' and t.kind==8 and t.value=='minecraft:decorated_pot' and 'sherds' not in d:d['sherds']=Tag(9,(8,['minecraft:brick']*4))
  if k=='id' and t.kind==8 and ':' in t.value and not t.value.startswith(('minecraft:','dungeons_arise:')):
   t.value=replace_item(t.value) if ('Count' in d or 'count' in d) else 'minecraft:skeleton'
  if t.kind==10:clean_nbt(t.value,k)
  elif t.kind==9 and t.value[0]==10:
   if k in {'Attributes','attributes'}:t.value=(10,[v for v in t.value[1] if v.get('Name',v.get('id',Tag(8,'minecraft:'))).value.startswith('minecraft:') and v.get('id',Tag(8,'')).value!='minecraft:skeleton'])
   for v in t.value[1]:clean_nbt(v,k)
def convert_nbt(raw):
 name,root=read(gzip.decompress(raw));d=root.value
 palettes=[d['palette'].value[1]] if 'palette' in d else [v[1] for v in d['palettes'].value[1]]
 for palette in palettes:
  for state in palette:
   old=state['Name'].value
   if old.startswith('minecraft:'):continue
   new=block_id(old);state['Name']=Tag(8,new)
   allowed=set()
   if new.endswith('_stairs'):allowed={'facing','half','shape','waterlogged'}
   elif new.endswith('_slab'):allowed={'type','waterlogged'}
   elif new.endswith('_wall'):allowed={'north','south','east','west','up','waterlogged'}
   elif new.endswith(('_fence','iron_bars')):allowed={'north','south','east','west','waterlogged'}
   elif new.endswith('chest'):allowed={'facing','type','waterlogged'}
   elif new.endswith('ladder'):allowed={'facing','waterlogged'}
   if 'Properties' in state:
    state['Properties'].value={k:v for k,v in state['Properties'].value.items() if k in allowed}
    if new.endswith('_slab') and state['Properties'].value.get('type',Tag(8,'bottom')).value not in {'top','bottom','double'}:state['Properties'].value['type']=Tag(8,'bottom')
    if not state['Properties'].value:del state['Properties']
 for b in d.get('blocks',Tag(9,(10,[]))).value[1]:
  if 'nbt' not in b:continue
  bd=b['nbt'].value;ident=bd.get('id',Tag(8,'')).value
  if ident and not ident.startswith('minecraft:'):
   if ident=='create:copycat' and 'Material' in bd:
    material=bd['Material'].value
    if material.get('Name',Tag(8,'')).value.startswith('minecraft:'):
     import copy
     for palette in palettes:palette.append(copy.deepcopy(material))
     b['state']=Tag(3,len(palettes[0])-1)
   # A substituted block entity gets a clean vanilla payload.
   state=palettes[0][b['state'].value]['Name'].value
   entity={'minecraft:chest':'minecraft:chest','minecraft:spawner':'minecraft:mob_spawner','minecraft:flower_pot':'','minecraft:decorated_pot':'minecraft:decorated_pot','minecraft:oak_sign':'minecraft:sign'}.get(state,'')
   if entity:b['nbt']=Tag(10,{'id':Tag(8,entity),**{k:v for k,v in bd.items() if k in {'Items','LootTable','LootTableSeed','CustomName','Lock','SpawnData','SpawnPotentials','Delay','MinSpawnDelay','MaxSpawnDelay','SpawnCount','MaxNearbyEntities','RequiredPlayerRange','SpawnRange'}}})
   else:del b['nbt']
   stats['mod_block_entities']+=1
 # Mod-only embedded entities cannot spawn in vanilla.
 if 'entities' in d:
  d['entities'].value=(10,[e for e in d['entities'].value[1] if e.get('nbt',Tag(10,{})).value.get('id',Tag(8,'minecraft:')).value.startswith('minecraft:')])
 clean_nbt(d)
 # Keep source DataVersion: Minecraft's data fixer upgrades saved entity/item/block NBT.
 return gzip.compress(write(name,root),mtime=0)

def build():
 OUT.mkdir(exist_ok=True);RELEASE.mkdir(exist_ok=True)
 for f in SRC.rglob('*'):
  if not f.is_file():continue
  rel=f.relative_to(SRC);s=rel.as_posix()
  if any(v in s for v in ['/integrated_structure_spawners/','/integrated_structure_map_trades/','data/lootintegrations/','data/integrated_api/']):continue
  target=OUT/rel;target.parent.mkdir(parents=True,exist_ok=True)
  if f.suffix=='.json':save(target,process_json(rel,json.loads(f.read_text(encoding='utf-8'))))
  elif f.suffix=='.nbt':target.write_bytes(convert_nbt(f.read_bytes()));stats['nbt_templates']+=1
  elif f.name=='pack.mcmeta':save(target,{'pack':{'min_format':[121,0],'max_format':[121,0],'description':'Integrated Dungeons Arise — Vanilla/Paper 26.3'}})
  else:target.write_bytes(f.read_bytes())
  if stats['nbt_templates'] and stats['nbt_templates']%100==0:print('templates',stats['nbt_templates'],flush=True)
 save(RELEASE/'conversion-report.json',{'counts':dict(stats),'replacements':replacements})
 with zipfile.ZipFile(RELEASE/'IDA-Vanilla-26.3.zip','w',zipfile.ZIP_DEFLATED) as z:
  for f in sorted(OUT.rglob('*')):
   if f.is_file():z.write(f,f.relative_to(OUT).as_posix())
 print(dict(stats),flush=True)

if __name__=='__main__':build()
