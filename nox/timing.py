"""Fast combat profile: each telegraph, hazard delay and idle gap is <=40 ticks."""
from build import DP, OUT, NS, fn, js

def patch(name, replacements):
    p=DP/f'data/{NS}/function/{name}.mcfunction'
    content=p.read_text(encoding='utf-8')
    for before,after in replacements:
        assert before in content,(name,before)
        content=content.replace(before,after)
    fn(name,content.rstrip().splitlines())

def apply_fast_timing():
    patch('fight/begin',[('#next nx.next 45','#next nx.next 30')])
    patch('fight/phase3',[('#next nx.next 60','#next nx.next 20')])
    patch('skills/begin',[('#cast nx.cast 44','#cast nx.cast 30'),('#cast nx.cast 54','#cast nx.cast 30'),
                          ('#cast nx.cast 90','#cast nx.cast 72'),('#cast nx.cast 50','#cast nx.cast 30'),('#cast nx.cast 32','#cast nx.cast 24')])
    patch('skills/combo',[('#cast nx.cast 28','#cast nx.cast 20'),('#total nx.total 28','#total nx.total 20')])
    patch('skills/echo',[('nx.time 50','nx.time 30'),('2.5초','1.5초')])
    patch('skills/recover',[('#safe nx.safe 30','#safe nx.safe 25'),('#next nx.next 22','#next nx.next 5'),
                            ('#next nx.next 14','#next nx.next 5'),('#safe nx.safe 90','#safe nx.safe 35')])
    patch('skills/dash/end',[('#safe nx.safe 60','#safe nx.safe 30'),('#safe nx.safe 90','#safe nx.safe 35'),('#next nx.next 18','#next nx.next 5')])
    patch('puzzle/success',[('#safe nx.safe 120','#safe nx.safe 35'),('#next nx.next 120','#next nx.next 5'),('6초','1.75초')])
    patch('puzzle/tick',[('#puzzletime nx.tmp matches 100..','#puzzletime nx.tmp matches 40..')])
    patch('puzzle/pulse',[('nx.time 60','nx.time 30'),('3초','1.5초')])
    patch('puzzle/overload',[('nx.time 40','nx.time 30'),('2초','1.5초')])
    # Three-wave attack lasts 3.6s, but each individual warning lasts only 1.2s.
    patch('skills/casting',[('#cast nx.cast matches 60','#cast nx.cast matches 48'),('#cast nx.cast matches 30','#cast nx.cast matches 24')])
    for name in ['skills/ring_warn','skills/ring_hit']:
        patch(name,[('#cast nx.cast matches 60..','#cast nx.cast matches 48..'),
                    ('#cast nx.cast matches 30..59','#cast nx.cast matches 24..47'),
                    ('#cast nx.cast matches ..29','#cast nx.cast matches ..23')])
    # Seven one-second sectors: initial teaching sector + six damaging sectors.
    patch('skills/eclipse_begin',[('#cast nx.cast 280','#cast nx.cast 140')])
    patch('skills/eclipse_tick',[('#rot nx.tmp matches 40..','#rot nx.tmp matches 20..')])
    for i in range(8):
        patch(f'skills/eclipse/{i}',[('#rot nx.tmp matches ..20','#rot nx.tmp matches ..10'),
                                    ('#cast nx.cast matches ..240','#cast nx.cast matches ..120'),
                                    ('#rot nx.tmp matches 30','#rot nx.tmp matches 15')])
    # Preserve anticipation and follow-through within the shorter telegraphs.
    patch('visual/tick',[('#cast nx.cast matches 1..18','#cast nx.cast matches 1..8'),
                         ('execute if score #safe nx.safe matches 50..','execute if score #expose nx.expose matches 1 if score #safe nx.safe matches 11..')])
    patch('visual/frame/wind',[('#denom nx.tmp 18','#denom nx.tmp 8')])
    patch('visual/frame/impact',[('#frame nx.tmp 18','#frame nx.tmp 8'),('#eighteen nx.tmp 18','#eighteen nx.tmp 8')])
    patch('visual/frame/recover',[('#frame nx.tmp 30','#frame nx.tmp 25'),('#thirty nx.tmp 30','#thirty nx.tmp 25')])
    profile={'ticks_per_second':20,'maximum_single_wait_ticks':40,
             'telegraph_ticks':{'cleave_first':30,'cleave_second':20,'dash':24,'echo':30,'ring_normal':30,'ring_each_phase3_wave':24,'eclipse_first_damage':35},
             'hazard_delay_ticks':{'puzzle_echo':30,'bell_overload':30},
             'interval_ticks':{'puzzle_echo_creation':40,'eclipse_rotation':20,'eclipse_bell_shelter':10},
             'recovery_plus_idle_ticks':{'normal':30,'dash':35,'wall_crash':40,'puzzle_success':40,'eclipse_end':40},
             'attack_duration_ticks':{'phase3_three_waves':72,'eclipse_seven_sectors':140},
             'note':'Full multi-stage attack durations are not idle waits. Entry grace and player-controlled puzzle completion are unchanged.'}
    for field in ['telegraph_ticks','hazard_delay_ticks','interval_ticks','recovery_plus_idle_ticks']:
        assert all(v<=40 for v in profile[field].values()),field
    js(OUT/'timing-profile.json',profile)
