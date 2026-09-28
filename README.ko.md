# 극한 난이도 플러그인 패키지

결과물: `release/extreme/`. `plugins/` 안에 JAR와 실제로 읽히는 설정 폴더를 함께 배치합니다.

## 버전과 출처

- mcMMO: 공식 Maven 저장소의 최신 정식 버전 **2.3.001**에 해당하는 소스 커밋 `c69f1fcc8072cc6ca032d366290b1161f9034a35`를 빌드합니다.
- 사용자가 제공한 `mcMMO-master.zip`은 **2.3.002-SNAPSHOT**입니다. 원본은 보존하고 정식 버전 소스를 별도로 받았습니다.
- MythicMobs: 제공된 **5.13.0-aad3f1c9** JAR를 그대로 포함합니다. 소스가 제공되지 않았으므로 재컴파일한 파일이 아닙니다.
- MythicMobs 공식 5.13.0 변경 이력은 Minecraft 26.2 지원을 명시합니다. 전체 패키지의 실제 서버 구동 호환성은 별도로 검증해야 합니다.
- 빌드는 원래 프로젝트의 Java 17 바이트코드/API 설정을 유지합니다. 최신 서버를 실행할 Java 버전은 해당 서버 배포판 요구사항을 따르세요.

참조:
- https://nexus.neetgames.com/repository/maven-releases/com/gmail/nossr50/mcMMO/mcMMO/maven-metadata.xml
- https://github.com/mcMMO-Dev/mcMMO/commit/c69f1fcc8072cc6ca032d366290b1161f9034a35
- https://wiki.mythiccraft.io/mythicmobs/changelogs/Changelogs
- https://wiki.mythiccraft.io/mythicmobs/Random-Spawns

## 난이도

- 모든 스킬 경험치 획득량 20%, 초반 경험치 보너스 해제.
- 사망 시 해당 기능이 지원되는 17개 스킬 레벨 75% 손실, 레벨 보호 구간 없음.
- PvP 및 번식 경험치 0, 기존 스포너/알 경험치 0 유지.
- 능력 쿨다운 3배, 최대 지속시간 5초, 추가 도구 내구도 소모 3.
- 키메라 날개 탈출 불가, 파티 아군 피해 허용, 파티 경험치 배율 보너스 제거.
- 오버월드 좀비/스켈레톤/거미 자연 생성의 65%를 강화 개체로 교체.
- 네더 위더 스켈레톤 80%, 엔드 엔더맨 60% 교체.
- 강화 개체 체력 90~200, 기본 공격력 설정 12~24, 이동속도 및 추적 거리 증가. 실피해는 몹 종류/갑옷/서버 난이도 영향을 받습니다.
- 거미 공격에 독 II 4초. 강화 몬스터 기본 드롭 제거.
- 몬스터 수를 늘리는 ADD 방식 대신 자연 생성 REPLACE 사용, 생성 상한 준수.

## 설치

1. 서버를 종료하고 기존 `plugins/mcMMO`, `plugins/MythicMobs`와 월드를 백업합니다.
2. 기존 mcMMO/MythicMobs JAR를 서버 밖으로 옮겨 같은 플러그인의 중복 로딩을 방지합니다.
3. `release/extreme/plugins/`의 내용 전체를 서버 `plugins/`로 복사합니다. 같은 이름의 설정은 이 프리셋으로 덮어씁니다.
4. 서버 `server.properties`의 `difficulty`를 `hard`로 변경합니다. 제공된 `.fragment`는 참고용이며 서버가 자동으로 읽지 않습니다.
5. 월드 이름이 `world`, `world_nether`, `world_the_end`가 아니면 `MythicMobs/RandomSpawns/Extreme.yml`의 `Worlds`를 수정합니다.
6. 기존 커스텀 RandomSpawns 규칙과 충돌 여부를 확인합니다. 기본 예제 규칙 파일은 빈 파일로 제공됩니다.
7. 서버를 완전히 재시작합니다. mcMMO에는 Bukkit `/reload`를 사용하지 않습니다.
8. 콘솔에서 두 플러그인의 활성화와 MythicMobs 설정 오류를 확인하고, 테스트 월드에서 `/mm mobs spawn ExtremeRevenant 1`로 몬스터를 확인합니다. 자연 출현은 별도로 확인합니다.

사망 페널티는 게임 내 플레이어 데이터에 실제로 적용됩니다. OP 또는 면제 권한이 있는 계정은 페널티가 다르게 적용될 수 있으므로 일반 계정으로 확인하세요.

## 재현

Python 3 + PyYAML, JDK, Maven이 필요합니다. 작업 폴더에서 실행합니다.

```powershell
.\.tools\apache-maven-3.9.11\bin\mvn.cmd -B -ntp -s build-settings.xml -f source/mcMMO-c69f1fcc8072cc6ca032d366290b1161f9034a35/pom.xml clean verify
python assemble.py
```

`release/build-release.log`는 빌드/테스트 기록, `release/extreme/SHA256.json`은 배포 파일 해시입니다. 자동 조립 검사는 YAML 파싱, 몬스터 참조, 설정값 및 JAR 무결성을 확인합니다. 실제 서버를 실행하는 테스트는 아닙니다.

기본 Maven 테스트 프로필은 upstream 설정에 따라 `skip`, `stress`, `docker` 그룹을 제외합니다. Docker 데이터베이스 통합 테스트와 스트레스 테스트는 기본 검증에 포함되지 않습니다. `build.ps1`로 빌드·검증·ZIP 패키징을 다시 실행할 수 있습니다.
