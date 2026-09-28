# MythicMobs 5.13.0-local263-r2

대상: Paper 26.3 빌드 41 / Java 25. 제공된 원본 5.13.0 JAR 기반 로컬 바이너리 호환 패치입니다.

## r1 이후 수정

- 엔티티 제거 패킷의 `getEntityIds()` 호출을 26.3의 `entityIds()`로 변경했습니다. 첨부 로그에서 424회 반복된 오류의 원인입니다.
- `RegistryFriendlyByteBuf.writeCollection()`이 제거되어 발생한 발광 팀 초기화 오류를 수정했습니다. 같은 형식(VarInt 길이 + 각 항목 인코딩)으로 기록하는 보조 메서드를 추가했고, 팀 초기화/색상 적용의 3개 호출 지점에 적용했습니다.
- r1의 26.3 버전 인식 수정도 포함합니다.

## 설치

서버를 종료하고 `plugins`의 기존 MythicMobs JAR를 서버 밖으로 옮긴 뒤, `MythicMobs-5.13.0-local263-r2.jar` 하나만 넣고 재시작하세요. 설정과 플레이어 데이터는 유지합니다. 이번 파일은 Paper 26.3용이며 다른 버전에 사용하지 마세요.

## 검증 범위

Paper 26.3-41, Java 25, Windows의 로컬 서버에서 검사합니다. 실제 제거 패킷 콜백을 호출하고, 발광 팀 패킷 인코딩·디코딩이 플레이어 전송 직전까지 진행되는지 확인합니다. 테스트에는 접속한 플레이어가 없으므로 클라이언트 수신 및 표시까지 검증한 것은 아닙니다. 기존 활성화·몬스터 5종 생성·체력·자연 생성 교체 검사도 재실행합니다.

로그: `release/mythic263-r2-smoke.log`. 테스트용 SmokeProbe는 배포하지 않습니다.

전체 NMS 기능이나 다른 플러그인 조합의 완전한 호환성을 의미하지 않습니다. 원본 예제 대화 경고와 종료 시 작업 등록 경고는 이 수정 범위에 포함하지 않았습니다.

## 별도 로그 문제

`nova_structures:mineshaft_jaggedpeak` 구조물 누락과 `nova_structures:hamlet/jockey` 풀 누락은 데이터팩 측 오류입니다. 이 JAR 교체로 해결되지 않습니다. 해당 데이터팩 파일이 현재 작업 폴더에 없어 수정하지 않았습니다.

## 재현

`compat/build.ps1` 실행. `PatchMythic.java`와 `BufferCompat.java`를 컴파일하여 원본 SHA-256이 일치하는 JAR에만 적용합니다. Paper 26.3 서버 JAR와 라이브러리, JDK 25, ASM 9.9.1이 필요합니다.

SHA-256: `364e830f98d5ebe949518b4af46fb6b18497f378d17577c843cbaff7bf78959a`
