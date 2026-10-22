import json
from pathlib import Path
b=Path('eve-ko');m=json.loads((b/'memory.json').read_text('utf-8'));p=json.loads((b/'pending.json').read_text('utf-8'));left=[s for s in p if s not in m];print('remaining',len(left));print('\n'.join(repr(s[:180]) for s in left[:15]))
