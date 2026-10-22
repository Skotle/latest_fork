from pathlib import Path
import json,zipfile,re
b=Path('eve-ko');s=next((b/'source').iterdir());r=b/'instance-overlay/config/openloader/resources/zz_explorers_eve_ko';report=json.loads((b/'coverage.json').read_text('utf-8'));rows=[]
for entry in report['sources']:
 if not entry['source'].endswith('.jar'):continue
 with zipfile.ZipFile(s/'mods'/entry['source']) as z:en=json.loads(z.read(entry['path']))
 ko=json.loads((r/entry['path'].replace('en_us','ko_kr')).read_text('utf-8'))
 for k,v in en.items():
  if v==ko[k] and re.search('[A-Za-z]',v):rows.append((entry['path'],k,v))
print('Unchanged',len(rows))
for row in rows:print(repr(row))
