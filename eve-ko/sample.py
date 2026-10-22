import json
from pathlib import Path
b=Path('eve-ko');m=json.loads((b/'memory.json').read_text('utf-8'));p=json.loads((b/'pending.json').read_text('utf-8'))
for s in p:
 if s in m and ('Wither Storm' in s or "Explorer's" in s):print(s[:180],'=>',m[s][:220])
