from pathlib import Path
import json,zipfile
b=Path('eve-ko');s=next((b/'source').iterdir());r=b/'instance-overlay/config/openloader/resources/zz_explorers_eve_ko'
for mod,ns,keys in [('twilightforest-1.19.4-4.2.1696-universal.jar','twilightforest',['advancement.twilightforest.hill1.desc','death.attack.twilightforest.yeeted']),('FallingTree-1.19.4-3.13.1.jar','fallingtree',['text.autoconfig.fallingtree.option.tools.speedMultiplicand.@Tooltip'])]:
 with zipfile.ZipFile(s/'mods'/mod) as z:d=json.loads(z.read(f'assets/{ns}/lang/en_us.json'))
 ko=json.loads((r/f'assets/{ns}/lang/ko_kr.json').read_text('utf-8'))
 for k in keys:print(repr(d[k]),repr(ko[k]))
