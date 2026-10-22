from pathlib import Path
import zipfile,json,hashlib
b=Path('eve-ko');o=b/'instance-overlay'
with zipfile.ZipFile(b/'ExplorerEve-Korean-Full.zip') as z:
 files=[p for p in o.rglob('*') if p.is_file()]
 mismatches=[str(p) for p in files if hashlib.sha256(p.read_bytes()).digest()!=hashlib.sha256(z.read(p.relative_to(o).as_posix())).digest()]
 print('Packaged overlay files:',len(files),'Content mismatches:',len(mismatches))
 assert not mismatches
 for ns,key in [('xaerominimap','gui.xaero_add_edit'),('aether','gui.aether.book_of_lore.item')]:
  d=json.loads(z.read(f'config/openloader/resources/zz_explorers_eve_ko/assets/{ns}/lang/ko_kr.json'))
  assert any('\uac00'<=c<='\ud7a3' for c in d[key])
r=json.loads((b/'coverage.json').read_text('utf-8'));print('Mods:',r['mods_scanned'],'Language files:',r['language_files'])
for p in b.glob('ExplorerEve-*.zip'):print(p.name,p.stat().st_size)
