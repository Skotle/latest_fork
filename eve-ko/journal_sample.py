from pathlib import Path
import zipfile
s=next(Path('eve-ko/source').iterdir())
with zipfile.ZipFile(s/'mods/blue_skies-1.19.4-1.3.25.jar') as z:
 print(z.read('data/blue_skies/blue_skies/journal/entries/alchemist.json').decode()[:4500])
 print(z.read('assets/blue_skies/blue_skies/journal_lang/en_us.json').decode()[:500])
