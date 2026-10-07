"""Validate the model/resource graph and assemble a two-pack installation bundle."""
import hashlib
import json
import math
import re
import zipfile
from pathlib import Path
from PIL import Image
from bosses import BOSSES, DATA
from boss_visuals import BASE, RESOURCE, OUTPUT, make_rig, write_json

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def validate():
 models=list((RESOURCE/'assets/ida_boss/models/boss').rglob('*.json'))
 entries=list((RESOURCE/'assets/ida_boss/items/boss').rglob('*.json'))
 expected=sum(len(make_rig(b['id']).parts) for b in BOSSES)
 assert len(models)==len(entries)==expected
 signatures=set()
 for b in BOSSES:
  rig=make_rig(b['id'])
  signature=json.dumps(rig.parts,sort_keys=True)
  assert signature not in signatures,b['id']
  signatures.add(signature)
  for phase in [1,2]:
   for pose in ['idle','walk','wind','recover']:
    for frame in range(4):assert (DATA/f'function/boss/visual/{b["id"]}/{phase}_{pose}_{frame}.mcfunction').is_file()
 for path in RESOURCE.rglob('*.json'):
  data=json.loads(path.read_text(encoding='utf-8'))
  if '/items/' in path.as_posix() and 'model' in data and data['model']['type']=='minecraft:model':
   ns,rel=data['model']['model'].split(':')
   assert (RESOURCE/f'assets/{ns}/models/{rel}.json').is_file(),path
  if '/models/' in path.as_posix():
   for tex in data['textures'].values():
    ns,rel=tex.split(':')
    assert (RESOURCE/f'assets/{ns}/textures/{rel}.png').is_file(),(path,tex)
   for e in data['elements']:
    assert all(-16<=v<=32 for v in e['from']+e['to']),path
    assert all(a<b for a,b in zip(e['from'],e['to'])),path
    assert set(e['faces'])=={'up','down','north','south','east','west'}
    for face in e['faces'].values():
     assert face['texture']=='#atlas' and all(0<=v<=16 for v in face['uv'])
 for p in RESOURCE.rglob('*.png'):
  with Image.open(p) as im:im.verify()
 count=0
 for p in (DATA/'function/boss').rglob('*.mcfunction'):
  for ident in re.findall(r'ida_boss:boss/[a-z0-9_/-]+',p.read_text(encoding='utf-8')):
   assert (RESOURCE/f'assets/ida_boss/items/{ident.split(":")[1]}.json').is_file(),(p,ident)
  for ident in re.findall(r'function (dungeons_arise:boss/[a-z0-9_/-]+)(?:\s|$)',p.read_text(encoding='utf-8')):
   assert (DATA/f'function/{ident.split(":")[1]}.mcfunction').is_file(),(p,ident)
  count+=1
 report={'bosses':22,'unique_rigs':len(signatures),'models':len(models),'item_entries':len(entries),
  'textures':22,'pose_functions':704,'boss_functions':count,'resource_references_complete':True,
  'valid_geometry_bounds':True,'resource_pack_format':[97,1],
  'limitations':['Static resource graph and software-rendered preview; not a Minecraft client render test.']}
 write_json(OUTPUT/'boss-model-static-validation.json',report)
 return report

def release():
 report=validate()
 datapack=OUTPUT/'IDA-Vanilla-26.3-Bosses-Models.zip'
 engine_path=OUTPUT/'boss-model-validation-results.json'
 engine=json.loads(engine_path.read_text(encoding='utf-8'))
 tested=BASE.parent/'.tools/boss-model-test'/engine['world']/'datapacks/IDA.zip'
 assert engine['command_errors']==0 and engine['death_cleanup']
 assert sha(tested)==sha(datapack),'The packaged datapack differs from the engine-tested datapack'
 engine['datapack_sha256']=sha(tested)
 write_json(engine_path,engine)
 original=OUTPUT/'Integrated-Resource-Pack-with-Ancient-Artifacts-2.zip'
 merged=OUTPUT/'IDA-Integrated-Boss-Resources-26.3.zip'
 original_hash=sha(original)
 with zipfile.ZipFile(original) as source,zipfile.ZipFile(merged,'w',zipfile.ZIP_DEFLATED) as dest:
  for info in source.infolist():
   if info.is_dir() or info.filename=='pack.mcmeta':continue
   assert not info.filename.startswith('/') and '..' not in Path(info.filename).parts
   assert not info.filename.startswith('assets/ida_boss/'),info.filename
   dest.writestr(info,source.read(info.filename))
  for p in sorted(RESOURCE.rglob('*')):
   if p.is_file() and p.name!='pack.mcmeta':dest.write(p,p.relative_to(RESOURCE).as_posix())
  meta=json.loads((RESOURCE/'pack.mcmeta').read_text(encoding='utf-8'))
  meta['pack']['description']='Integrated RP + IDA Boss Models — Minecraft Java 26.3'
  dest.writestr('pack.mcmeta',json.dumps(meta,ensure_ascii=False,indent=2))
 assert sha(original)==original_hash
 with zipfile.ZipFile(original) as source,zipfile.ZipFile(merged) as dest:
  for n in source.namelist():
   if n!='pack.mcmeta' and not n.endswith('/'):assert source.read(n)==dest.read(n),n
 guide='''# IDA 26.3 — 전용 보스 모델판

클라이언트 모드와 서버 플러그인 없이 데이터팩 + 리소스팩으로 작동합니다.
22종 전용 3D 모델, 179개 관절 부품, 대기/이동/공격 준비/회복 동작,
2페이즈 일부 코어·고리·검 변화, 직선/부채꼴/십자/고리/다중 표식 공격을 추가했습니다.

## 설치

1. 월드를 백업하고 기존 IDA 데이터팩을 `IDA-Vanilla-26.3-Bosses-Models.zip`으로 교체합니다.
   같은 IDA 데이터팩을 두 개 함께 활성화하지 마세요. 압축을 풀지 말고 월드의 `datapacks`에 넣습니다.
2. `IDA-Integrated-Boss-Resources-26.3.zip`을 클라이언트의 `resourcepacks`에 넣고 적용합니다.
   기존 통합 리소스팩 전체가 포함된 합본이므로 이 리소스팩 하나면 됩니다.
   같은 리소스를 덮는 다른 리소스팩보다 위에 두세요. 서버에서는 모든 플레이어에게 이 합본을 배포해야 합니다.
3. Minecraft Java 26.3에서 월드를 열고 `/reload`를 실행합니다.
4. 넓은 시험 공간에서 `/function dungeons_arise:boss/admin/spawn/typhon`으로 확인합니다.
   소환 명령은 시험용이며 반복하면 여러 보스가 생깁니다.
   `/function dungeons_arise:boss/admin/remove_nearby`로 주변 시험 보스와 기록을 정리합니다.

## 원본과 별도 외형 팩

기존 통합 리소스팩 ZIP은 수정하지 않았습니다. 새 합본에서 원래 리소스 파일 내용도 그대로 유지했습니다.
기존 보스 데이터팩은 `IDA-Vanilla-26.3-Bosses-before-models.zip`으로 보관했습니다.
`IDA-Boss-Models-26.3.zip`은 보스 외형만 담은 별도 팩입니다. 합본을 쓸 때는 추가로 적용하지 않습니다.
기존 통합 팩을 따로 유지하려면 보스 외형 팩을 그 위에 놓는 방법도 사용할 수 있습니다.

## 구현과 확인 범위

원래 몹의 AI·체력·무기·갑옷·보상을 유지하면서 보이지 않게 하고, 별도 item_display 부품으로 전용 외형을 표시합니다.
갑옷과 무기는 숨김 전용 리소스로 렌더링하며 실제 공격·방어 기능을 유지합니다.
시전 중에는 AI를 멈추고 공격 준비 동작을 표시하며, 공격 후 1초간 회복 동작과 빈틈을 제공합니다.
고리형 공격은 보스 중심 반경 3~6블록이 위험하며 안쪽과 바깥쪽이 안전합니다.
직선 공격은 옆으로 피하고, 여러 독·폭발 및 십자 표식은 표시된 영역에서 벗어나세요.
일반 경고는 2초, 태양왕의 낙인은 3초입니다. 중첩 표식은 한 스킬에서 피해를 중복 적용하지 않습니다.
모델은 매 틱 보스를 따라가며 관절 자세는 초당 4회, 5틱 보간으로 갱신합니다.
전투 중단·처치 시 부품을 정리하고, 모델이 모두 없어진 경우 다시 생성합니다.

피격과 충돌은 보이지 않는 원래 몹이 담당합니다. 몸체를 공격하세요.
거미·날개형·껍질형은 모델 높이와 원래 몹의 크기를 조정했지만, 날개·돌출 무기·다리에는 별도 피격 판정이 없습니다.
리소스팩 미적용 상태에서는 보스가 올바르게 보이지 않습니다.
기존 몹을 전역으로 교체하는 리소스가 아니라 보스 전용 네임스페이스이므로 일반 몹의 외형은 유지합니다.

실제 공식 바닐라 Minecraft 26.3 서버에서 명령 실행·22종 소환·704개 자세 함수·20개 특수 공격 함수·
시전과 회복·2페이즈·경계 복귀·리로드·모델 재생성·중단과 처치 후 정리를 검사합니다.
실행 결과는 `boss-model-validation-results.json`, 리소스와 모델 참조 검사 결과는 `boss-model-static-validation.json`입니다.
시험 전용 네트워크 에이전트와 Java 런타임은 배포 데이터팩/리소스팩에 포함하지 않습니다.
미리보기 PNG/GIF는 실제 생성 모델의 형상을 별도 렌더러로 그린 것이며 Minecraft 게임 화면은 아닙니다.
클라이언트 접속과 렌더링, 갑옷 숨김, 피격 위치, 실제 플레이어 피해, 멀티플레이 밸런스는 게임 내 확인이 필요합니다.
기존 `boss-validation-results.json`은 이번 모델판 이전의 Paper 검증 결과입니다.

## 재현

`python ida26/bosses.py` — 모델 리소스/관절 함수/데이터팩과 별도 외형 팩 생성
`python ida26/boss_model_preview.py` — 모델 미리보기 생성 (Pillow 필요)
`python ida26/boss_guide.py` — 기존 설치·보스 목록 갱신
`python ida26/boss_models_smoke.py` — 준비된 로컬 Java 25/26.3 시험 서버에서 엔진 검증
`python ida26/boss_models_release.py` — 정적 검사/합본 리소스팩/배포 묶음 생성 (Pillow 필요)
'''
 (OUTPUT/'보스모델판-설치안내.md').write_text(guide,encoding='utf-8')
 files=[OUTPUT/n for n in ['IDA-Vanilla-26.3-Bosses-Models.zip','IDA-Integrated-Boss-Resources-26.3.zip',
  '보스모델판-설치안내.md','보스판-설치와목록.md','boss-model-validation-results.json',
  'boss-model-static-validation.json','boss-models-preview.png','boss-models-all.png','boss-model-animation.gif']]
 for p in files:
  assert p.is_file(),p
  if p.suffix=='.zip':
   with zipfile.ZipFile(p) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(set(z.namelist()))
    assert not any(n.endswith(('.jar','.class')) for n in z.namelist())
 write_json(OUTPUT/'boss-model-release-sha256.json',{p.name:sha(p) for p in files})
 bundle=OUTPUT/'IDA-Boss-Models-26.3-Bundle.zip'
 with zipfile.ZipFile(bundle,'w',zipfile.ZIP_DEFLATED) as z:
  for p in files+[OUTPUT/'boss-model-release-sha256.json']:z.write(p,p.name)
 with zipfile.ZipFile(bundle) as z:assert z.testzip() is None
 print(json.dumps({'bundle':str(bundle),'static_validation':report,'original_resources_unchanged':True},ensure_ascii=False,indent=2))

if __name__=='__main__':release()
