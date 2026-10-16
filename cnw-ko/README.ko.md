# Create New World 4.0.12 한국어 번역 팩

대상: Minecraft 1.21.1 / NeoForge 21.1.248 / Create New World 4.0.12.

## 제공 파일

- `CNW-Korean-Full-4.0.12.zip`: 퀘스트, 언어 파일, 한국어 문구로 수정한 KubeJS 스크립트를 포함한 설치용 통합 팩.
- `CNW-Korean-Resources-4.0.12.zip`: 모드 UI·아이템명·메뉴용 단독 리소스팩. 퀘스트 본문과 스크립트 안내는 포함하지 않음.
- `instance-overlay/`: 통합 팩에 들어가는 파일을 풀어 둔 편집용 폴더.
- `CNW-Original-Files-4.0.12.zip`: 이 패치가 덮어쓰는 기존 파일의 원본. 사용자 환경의 수정본 백업을 대신하지 않음.
- `translations.tsv`: 원문과 번역을 비교하는 UTF-8 편집·검수용 표.
- `coverage.json`: 포함 파일, 모드별 누락 키 수, 검증 범위.
- `validation.json`: 파일 형식·스크립트 구문·압축 검사 결과.

## 통합 팩 설치

1. 게임과 서버를 종료하고 인스턴스의 `config`와 `kubejs` 폴더를 백업합니다.
2. CurseForge에서 해당 인스턴스의 폴더를 엽니다.
3. `CNW-Korean-Full-4.0.12.zip`의 `config`와 `kubejs`를 인스턴스 폴더에 복사하고 같은 경로의 파일을 덮어씁니다. `mods` 폴더와 나란히 놓이는 구조입니다.
4. 게임을 다시 실행하고 언어를 한국어로 설정합니다. 시작 스크립트가 포함되므로 게임 전체 재시작이 필요합니다.
5. 서버에서도 한국어 진행 알림·JEI 설명·규칙·복구 문구를 사용하려면 서버에도 같은 버전의 패치를 적용하고 재시작합니다. 서버 스크립트의 직접 입력 문구는 접속자의 언어와 관계없이 한국어로 표시됩니다.

통합 팩에는 KubeJS assets 언어 파일이 있으므로 단독 리소스팩을 추가 적용할 필요가 없습니다. 기존 진행도 파일이나 퀘스트 ID는 변경하지 않습니다. 초기 실행 시 퀘스트 한국어 파일이 로드되는지 실제 게임에서 확인해야 합니다.

## 리소스팩만 설치

`CNW-Korean-Resources-4.0.12.zip`을 인스턴스의 `resourcepacks` 폴더에 넣고 게임에서 활성화한 뒤 한국어를 선택합니다. 다른 번역 팩보다 위에 배치하면 이 팩의 번역이 우선합니다. 이 방식만으로는 퀘스트 본문·직접 입력된 툴팁·진행 알림이 번역되지 않습니다.

## 번역 범위와 상태

모드팩 전용 퀘스트, 진행·연구 조건, 단계 해금 알림, JEI 설명, 규칙, 복구 알림, 커스텀 아이템·블록 이름, CNW 메뉴, Collapsible Groups를 포함합니다. 기본 모드 중 Northstar, FTB Quests, Create Aeronautics Automated Logistics, Create Enchantment Industry, Custom Machinery, Create Big Cannons, Create Diesel Generators, Create Propulsion, Create Quality of Life, Block Factory's Bosses의 기존 한국어 파일에 없는 키도 포함합니다. 모드 자체에 이미 있는 한국어 번역은 모드 JAR에서 계속 사용합니다.

Google Translate 기계 번역에 일부 수동 용어를 적용한 **검수 전 초안**입니다. 영어 원문을 외부 번역 서비스로 처리했으며, 문맥·고유명사·Create 용어는 추가 검수가 필요합니다. `translation-memory.json`과 `translations.tsv`로 원문을 대조할 수 있습니다. `build_pack.py`는 외부 번역 서비스를 사용하는 제작 도구이며 게임 실행에 필요하지 않습니다.

모든 모드의 완역은 아닙니다. Chipped 등 우선순위 밖 모드, FancyMenu의 별도 레이아웃 직접 입력 문구, 이미지에 그려진 글자, 셰이더 문구는 이번 패치에 포함하지 않았습니다. 기존 셰이더에는 한국어 언어 파일이 있습니다.

정적 검증과 실제 게임 실행 검증은 다릅니다. 이 팩은 게임을 실행해 확인하지 않았습니다. 메뉴 줄바꿈, 퀘스트 화면, 아이템 이름, JEI 설명, 단계 해금/복구 알림을 새 테스트 월드에서 점검한 뒤 기존 월드에 사용하는 것을 권장합니다.

## 되돌리기

게임과 서버를 종료하고 사용자 백업을 복원합니다. 백업이 없다면 `CNW-Original-Files-4.0.12.zip`으로 원본 스크립트와 퀘스트 챕터를 복원하고, `coverage.json`에 기록된 이 패치의 `ko_kr` 파일만 제거합니다. 다른 번역 팩이나 사용자가 원래 가지고 있던 한국어 파일을 함께 삭제하지 않도록 주의합니다. 단독 리소스팩은 비활성화하거나 해당 ZIP을 제거합니다.

이 팩은 원본 모드 JAR·텍스처·음원·월드 데이터를 재배포하지 않습니다. 원본 모드팩의 버전이 바뀌면 스크립트 덮어쓰기를 피하고 차이를 먼저 확인해야 합니다.
