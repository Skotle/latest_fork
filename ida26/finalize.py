"""Rebuild JSON after conversion; add native 26.3 map trades and verify references."""
import collections,json,zipfile
import build as b

for f in b.SRC.rglob('*.json'):
 rel=f.relative_to(b.SRC);s=rel.as_posix()
 if any(v in s for v in ['/integrated_structure_spawners/','/integrated_structure_map_trades/','data/lootintegrations/','data/integrated_api/']):continue
 b.save(b.OUT/rel,b.process_json(rel,json.loads(f.read_text(encoding='utf-8'))))
f=next((b.SRC/'data/integrated_api/integrated_structure_map_trades').glob('*.json'))
maps=json.loads(f.read_text());tags=collections.defaultdict(list)
trade_root=b.OUT/'data/dungeons_arise/villager_trade'
for stale in trade_root.glob('*.json'):stale.unlink()
def trade(m,tag):
 name=tag.split('/')[0]+'/'+m['structure'].split(':')[1]+'_map';ident='dungeons_arise:'+name
 b.save(b.OUT/f'data/dungeons_arise/villager_trade/{name}.json',{
  'wants':{'id':'minecraft:emerald','count':m['emeraldsRequired']},
  'additional_wants':{'id':'minecraft:compass'},'gives':{'id':'minecraft:filled_map'},
  'max_uses':m['tradesAllowed'],'xp':m['xpReward'],'reputation_discount':.2,
  'given_item_modifier':[{'type':'minecraft:exploration_map','destination':m['structure'],'decoration':'minecraft:'+m['mapIcon'].lower(),'search_radius':m['spawnRegionSearchRadius']},
   {'type':'minecraft:filtered','item_filter':{'predicates':{'minecraft:map_id':{}}},'on_fail':{'type':'minecraft:discard'}},
   {'type':'minecraft:set_name','name':{'text':m['mapName']},'target':'item_name'}]})
 tags[tag].append(ident)
for m in maps['villagerMaps']['minecraft:cartographer']:trade(m,f"cartographer/level_{m['tradeLevel']}")
for m in maps['wanderingTraderMap']['common']:trade(m,'wandering_trader/common')
for tag,values in tags.items():b.save(b.OUT/f'data/minecraft/tags/villager_trade/{tag}.json',{'replace':False,'values':values})
deco=json.loads((b.OUT/'data/dungeons_arise/worldgen/template_pool/underworld/foundry/foundry_corridor_deco.json').read_text())
deco['name']='dungeons_arise:underworld/foundry/foundry_corridor_gears'
deco['elements']=[e for e in deco['elements'] if '/foundry_corridor_gear_' in e['element'].get('location','')]
b.save(b.OUT/'data/dungeons_arise/worldgen/template_pool/underworld/foundry/foundry_corridor_gears.json',deco)
report_path=b.RELEASE/'conversion-report.json'
report=json.loads(report_path.read_text(encoding='utf-8')) if report_path.exists() else {'counts':{},'replacements':{}}
report['counts']['native_map_trades']=sum(map(len,tags.values()))
report['replacements'].update(b.replacements)
b.save(report_path,report)
with zipfile.ZipFile(b.RELEASE/'IDA-Vanilla-26.3.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(b.OUT.rglob('*')):
  if f.is_file():z.write(f,f.relative_to(b.OUT).as_posix())
print('JSON fixes and native map trades built',dict(b.stats))
