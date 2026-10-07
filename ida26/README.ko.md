# IDA 26.3 변환 작업

사용자 제공 IDA-1.21.1.zip을 Minecraft Java 26.3의 바닐라/Paper용으로 변환합니다.
원본 ZIP은 수정하지 않으며, 통합 리소스팩의 바이트도 수정하지 않습니다.

산출물은 output 폴더에 있습니다. 설치 방법과 기능 차이는 output/설치안내.txt를 참고하세요.

빌드 순서(Python 3 표준 라이브러리만 필요):

```powershell
python ida26/build.py
python ida26/finalize.py
```

original 폴더는 원본 데이터팩을 풀어 놓은 입력입니다. nbt_io.py는 타입을 보존하는
NBT 입출력 모듈이며, build.py는 JSON/NBT 변환을 수행합니다. finalize.py는 지도 거래,
누락된 Foundry 장식 풀과 최종 ZIP을 생성합니다. repair_nbt.py는 저장 데이터의 추가
호환성 수정을 기존 변환 결과에 적용하는 보조 스크립트입니다.

검증에 사용한 런타임: Paper 26.3-41 / Java 25, 플러그인 없음.
이 PC의 Java NIO 로컬 연결 오류 때문에 TestNetworkAgent.java가 테스트에서만
TCP 리스너를 생략합니다. 게임의 데이터팩 로딩/리로드와 구조물 생성/전리품 명령은
실제 Paper 엔진에서 실행합니다. 테스트 에이전트는 배포 ZIP에 들어가지 않습니다.
클라이언트 접속/렌더링/장시간 플레이 테스트는 포함하지 않습니다.

## 전용 보스 모델판

데이터팩 + 리소스팩만으로 22종 전용 모델과 관절 애니메이션을 구현한 판은
`output/IDA-Boss-Models-26.3-Bundle.zip`입니다. 설치에는 묶음 안의
`IDA-Vanilla-26.3-Bosses-Models.zip`과 `IDA-Integrated-Boss-Resources-26.3.zip`을 사용합니다.
기존 통합 리소스팩 원본은 보존합니다. `output/보스모델판-설치안내.md`에 적용 방법과 피격 판정의 한계를 설명합니다.

```powershell
python ida26/bosses.py
python ida26/boss_model_preview.py
python ida26/boss_guide.py
python ida26/boss_models_smoke.py
python ida26/boss_models_release.py
```

미리보기와 리소스 정적 검사에는 Pillow가 필요합니다. `boss_models_smoke.py`는
`.tools/boss-model-test`에 준비한 공식 Minecraft 26.3 서버 JAR와 Java 25를 사용하며,
시험용 월드를 따로 생성합니다. 이번 판의 바닐라 엔진 검사 결과는
`output/boss-model-validation-results.json`입니다. 실제 클라이언트 렌더링은 검증하지 않았습니다.

공식 변경 내역: https://www.minecraft.net/en-us/article/minecraft-java-edition-26-3
