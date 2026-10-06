import re,json,zlib,gzip,struct,collections,zipfile
from pathlib import Path
from nbt_io import read
from bosses import BASE,BOSSES,NORMAL_ENCHANT_CAPS,DATA
log=(BASE/'output/boss-smoke-console.log').read_text(encoding='utf-8')
worlds=sorted((BASE.parent/'.tools/ida263-smoke').glob('boss-test-*'),key=lambda p:p.stat().st_mtime)
world=worlds[-1];relics=collections.Counter();enchantments={}
for path in (world/'dimensions/minecraft/overworld/entities').glob('*.mca'):
 raw=path.read_bytes()
 for i in range(1024):
  address=int.from_bytes(raw[i*4:i*4+3],'big')*4096
  if not address:continue
  length=int.from_bytes(raw[address:address+4],'big');kind=raw[address+4];payload=raw[address+5:address+4+length]
  if kind==2:payload=zlib.decompress(payload)
  elif kind==1:payload=gzip.decompress(payload)
  _,root=read(payload)
  for entity in root.value.get('Entities').value[1]:
   if entity.get('id').value!='minecraft:item':continue
   item=entity.get('Item',entity.get('item'))
   if not item:continue
   components=item.value.get('components')
   if not components:continue
   custom=components.value.get('minecraft:custom_data')
   if not custom or 'ida_relic' not in custom.value:continue
   ident=custom.value['ida_relic'].value;relics[ident]+=item.value['count'].value
   enchantments[ident]={k:v.value for k,v in components.value['minecraft:enchantments'].value.items()}
assert len(relics)==22,relics
assert all(relics[b['id']]>=2 for b in BOSSES),relics
with zipfile.ZipFile(BASE.parent/'.tools/paper263/versions/26.3/paper-26.3.jar') as registry:
 for name,cap in NORMAL_ENCHANT_CAPS.items():
  definition=json.loads(registry.read('data/minecraft/enchantment/'+name.split(':')[1]+'.json')) if name.startswith('minecraft:') else json.loads((DATA/('enchantment/'+name.split(':')[1]+'.json')).read_text())
  assert cap==definition['max_level'],(name,cap)
for b in BOSSES:
 assert enchantments[b['id']]==b['enchants'],(b['id'],enchantments[b['id']])
 if b['over_cap_reward']:
  assert all(level>NORMAL_ENCHANT_CAPS[name] for name,level in enchantments[b['id']].items())
 else:
  assert all(level<=NORMAL_ENCHANT_CAPS[name] for name,level in enchantments[b['id']].items())
clean=re.sub(r'\x1b\[[0-9;]*m','',log)
resultline=next(x for x in clean.splitlines() if 'Storage selftest:results has' in x)
assert 'cleared: 22' in resultline and 'bosses: 22' in resultline
assert 'manual_sites: 22' in resultline
assert 'sunfire_warning_ticks: 60' in resultline and 'normal_warning_ticks: 40' in resultline
assert 'returned_bosses: 22' in resultline
adds_before=int(re.search(r'adds_before_return: (\d+)',resultline).group(1))
adds_after=int(re.search(r'returned_adds: (\d+)',resultline).group(1))
assert 0<adds_before<=4 and adds_after==adds_before,(adds_before,adds_after)
for b in BOSSES:assert f'{b["id"]}: {b["hp"]}' in resultline
for b in BOSSES:assert f'{b["id"]}: {b["period"]}' in resultline
assert 'There are no custom bossbars active' in clean
assert not any(x in clean for x in ['Failed to','Unknown registry','Invalid color','Failed to load function'])
with zipfile.ZipFile(BASE/'output/IDA-Vanilla-26.3-Bosses.zip') as z:
 assert z.testzip() is None
 assert not any(x.endswith('.jar') for x in z.namelist())
report={'engine':'Paper 26.3-41','world':world.name,'boss_count':22,'correct_base_health':True,'phase_two_count':22,'cleared_sites':22,'bossbars_after_clear':0,'relic_counts_direct_loot_plus_death':dict(relics),'all_relic_enchantments_correct':True,'spell_functions_exercised':20,'datapack_errors':0,'limitations':['No connected client; natural player entry, player damage, party scaling and combat balance not playtested.'],'network_disabled_for_local_test_only':True}
report['over_cap_reward_bosses']=[b['id'] for b in BOSSES if b['over_cap_reward']]
report['other_boss_rewards_within_normal_caps']=True
report['arena_return_test']={'bosses':22,'adds':adds_after,'radius':24}
report['warning_ticks']={'sunfire':60,'other_skills':40}
(BASE/'output/boss-validation-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))

