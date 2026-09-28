"""Assemble the extreme-difficulty pack from pinned upstream artifacts."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile
import yaml

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'source/mcMMO-c69f1fcc8072cc6ca032d366290b1161f9034a35'
OUT = ROOT / 'release/extreme'
PLUGINS = OUT / 'plugins'


def write_yaml(relative, data):
    path = PLUGINS / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding='utf-8')


def assemble():
    built = SOURCE / 'target/mcMMO.jar'
    if not built.is_file():
        raise FileNotFoundError('Build mcMMO successfully before assembling the release.')
    config = yaml.safe_load((SOURCE / 'src/main/resources/config.yml').read_text(encoding='utf-8'))
    death = config['Hardcore']['Death_Stat_Loss']
    death['Penalty_Percentage'] = 75.0
    death['Level_Threshold'] = 0
    death['Enabled'] = dict.fromkeys(death['Enabled'], True)
    config['Items']['Chimaera_Wing']['Enabled'] = False
    config['Party']['FriendlyFire'] = True
    for key in ('ExpShare_bonus_base', 'ExpShare_bonus_increase', 'ExpShare_bonus_cap'):
        config['Party']['Sharing'][key] = 1.0
    for key, value in config['Abilities']['Cooldowns'].items():
        config['Abilities']['Cooldowns'][key] = value * 3
    for key in config['Abilities']['Max_Seconds']:
        config['Abilities']['Max_Seconds'][key] = 5
    config['Abilities']['Tools']['Durability_Loss'] = 3
    write_yaml('mcMMO/config.yml', config)
    xp = yaml.safe_load((SOURCE / 'src/main/resources/experience.yml').read_text(encoding='utf-8'))
    xp['EarlyGameBoost']['Enabled'] = False
    xp['Experience_Formula']['Multiplier']['Global'] = 0.2
    xp['Experience_Formula']['Multiplier']['PVP'] = 0.0
    xp['Experience_Formula']['Breeding']['Multiplier'] = 0.0
    write_yaml('mcMMO/experience.yml', xp)

    with zipfile.ZipFile(ROOT / 'MythicMobs-5.13.0.jar') as jar:
        spawning = yaml.safe_load(jar.read('config-spawning.yml'))
    spawning['Configuration']['RandomSpawning']['ReplaceObeysCap'] = True
    write_yaml('MythicMobs/config/config-spawning.yml', spawning)
    mobs, spawns = {}, {}
    definitions = [
        ('Revenant', 'ZOMBIE', 120, 16, 0.32, 0.65, 'world', 'IRON_SWORD'),
        ('Reaper', 'SKELETON', 90, 12, 0.30, 0.65, 'world', 'BOW'),
        ('Stalker', 'SPIDER', 100, 14, 0.38, 0.65, 'world', None),
        ('Executioner', 'WITHER_SKELETON', 180, 22, 0.32, 0.8, 'world_nether', 'DIAMOND_SWORD'),
        ('VoidHunter', 'ENDERMAN', 200, 24, 0.35, 0.6, 'world_the_end', None),
    ]
    for name, kind, health, damage, speed, chance, world, weapon in definitions:
        ident = 'Extreme' + name
        mob = {'Type': kind, 'Display': '&4' + name, 'Health': health, 'Damage': damage,
               'Options': {'MovementSpeed': speed, 'FollowRange': 40,
                           'PreventOtherDrops': True, 'PreventRandomEquipment': True,
                           'Despawn': True, 'KnockbackResistance': 0.35}}
        if weapon:
            mob['Equipment'] = [weapon + ' HAND', 'IRON_HELMET HEAD']
        if kind == 'SPIDER':
            mob['Skills'] = ['potion{type=POISON;duration=80;level=1} @trigger ~onAttack']
        mobs[ident] = mob
        spawns[ident + 'Spawn'] = {'Type': ident, 'Worlds': world, 'Chance': chance,
                                  'Priority': 10, 'Action': 'REPLACE', 'Reason': 'NATURAL',
                                  'Level': 1, 'UseWorldScaling': False,
                                  'Conditions': ['entitytype{t=' + kind + '} true']}
    write_yaml('MythicMobs/Mobs/Extreme.yml', mobs)
    write_yaml('MythicMobs/RandomSpawns/Extreme.yml', spawns)
    # Prevent bundled example random spawns being installed alongside the preset.
    write_yaml('MythicMobs/RandomSpawns/ExampleRandomSpawns.yml', {})
    shutil.copy2(ROOT / 'MythicMobs-5.13.0.jar', PLUGINS)
    shutil.copy2(built, PLUGINS / 'mcMMO-2.3.001.jar')
    shutil.copy2(ROOT / 'README.ko.md', OUT)
    (OUT / 'server.properties.fragment').write_text('difficulty=hard\n', encoding='utf-8')
    verify()
    manifest = {str(p.relative_to(OUT)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(OUT.rglob('*')) if p.is_file() and p.name != 'SHA256.json'}
    (OUT / 'SHA256.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')


def verify():
    for p in PLUGINS.rglob('*.yml'):
        assert isinstance(yaml.safe_load(p.read_text(encoding='utf-8')), dict), p
    cfg = yaml.safe_load((PLUGINS / 'mcMMO/config.yml').read_text(encoding='utf-8'))
    assert all(cfg['Hardcore']['Death_Stat_Loss']['Enabled'].values())
    assert cfg['Hardcore']['Death_Stat_Loss']['Penalty_Percentage'] == 75.0
    xp = yaml.safe_load((PLUGINS / 'mcMMO/experience.yml').read_text(encoding='utf-8'))
    assert xp['Experience_Formula']['Multiplier']['Global'] == 0.2
    assert xp['EarlyGameBoost']['Enabled'] is False
    original = yaml.safe_load((SOURCE / 'src/main/resources/config.yml').read_text(encoding='utf-8'))
    for ability, seconds in original['Abilities']['Cooldowns'].items():
        assert cfg['Abilities']['Cooldowns'][ability] == seconds * 3
    assert (PLUGINS / 'MythicMobs-5.13.0.jar').read_bytes() == (ROOT / 'MythicMobs-5.13.0.jar').read_bytes()
    mobs = yaml.safe_load((PLUGINS / 'MythicMobs/Mobs/Extreme.yml').read_text(encoding='utf-8'))
    rules = yaml.safe_load((PLUGINS / 'MythicMobs/RandomSpawns/Extreme.yml').read_text(encoding='utf-8'))
    assert len(mobs) == len(rules) == 5
    for rule in rules.values():
        assert rule['Type'] in mobs
        assert rule['Reason'] == 'NATURAL' and rule['Action'] == 'REPLACE'
        assert 0 < rule['Chance'] <= 1
    for p in PLUGINS.glob('*.jar'):
        with zipfile.ZipFile(p) as jar:
            assert jar.testzip() is None
            assert 'plugin.yml' in jar.namelist()
            metadata = yaml.safe_load(jar.read('plugin.yml'))
            if metadata['name'] == 'mcMMO':
                assert str(metadata['version']).startswith('2.3.001')
    print('Verified YAML structure, spawn references, difficulty settings and JAR integrity.')


if __name__ == '__main__':
    assemble()
