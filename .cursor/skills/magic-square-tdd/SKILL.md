---
name: magic-square-tdd
description: MagicSquare_xx Dual-Track TDD·ECB 개발 시 Agent가 따를 절차. TDD·entity/control/boundary 구현·D-*/U-* 테스트·MagicConstant·E001~E007 작업 시 사용.
---

# MagicSquare Dual-Track TDD

MagicSquare_1004 ECB + Dual-Track TDD 워크플로. `.cursorrules` · `docs/PRD.md`와 충돌 시 **PRD > Report > Skill > 코드**.

## Skill을 켜는 때

다음 중 **하나라도** 해당하면 본 Skill을 적용한다.

- 사용자가 TDD · RED/GREEN/REFACTOR · Dual-Track · ECB 구현을 요청
- `src/entity` · `src/control` · `src/boundary` 또는 `tests/**/test_d_*` · `test_u_*` 수정
- `D-*` · `U-*` 테스트 ID · MS4_RULE · `validate_grid` · `find_violations` 언급
- MagicConstant · E001~E007 · 10선 판정 · SC-1~3 · T01~T05 작업

**켜지 않을 때:** 문서만 작성 · README · git · Harness 골격만 수정 (테스트·도메인 코드 없음).

매 턴 선언 (한국어):

```
Phase: RED | GREEN | REFACTOR
Layer: entity | control | boundary
Track: Logic | UI
Test: D-XX | U-XX (해당 시)
```

---

## Logic Track vs UI Track

| | **Logic Track** | **UI Track** |
|---|---|---|
| **계층** | entity, control | boundary |
| **테스트 ID** | `D-*` | `U-*` |
| **파일** | `tests/{entity,control}/test_d_*.py` | `tests/boundary/test_u_*.py` |
| **Domain Mock** | **금지** — Grid·Axis·Rule 실객체 | N/A |
| **I/O Mock** | 금지 (Logic은 I/O 없음) | **허용** — stdin·파일·CLI |
| **의존** | entity ← control만 | boundary → control → entity |
| **오류** | MS4_RULE_01~06 (도메인) | E001~E007 (입력·형식) |

한 사이클에 **한 Layer · 한 Track**만 Green 목표.

---

## ECB · Mock · E001~E007

### ECB 의존

```
boundary → control → entity
```

| 계층 | 허용 | 금지 |
|---|---|---|
| **entity** | 순수 도메인·Rule | **모든 외부 import** (`entity → *`) |
| **control** | entity 호출·오케스트레이션 | boundary import, I/O |
| **boundary** | control 위임·파싱·E001~E007 | entity 직접 Rule 우회 |

### Mock

| 대상 | Logic | UI |
|---|---|---|
| Grid / Axis / Rule | **금지** | — |
| control use case | **금지** (integration은 실제 control) | **허용** (boundary 단위 테스트) |
| stdin / 파일 / CLI | — | **허용** |

### E001~E007 (boundary 전용)

| 코드 | entity | control | boundary |
|---|---|---|---|
| E001~E005 | **처리 금지** | 위임 전 차단 가정 | **검출·반환** |
| E006~E007 | **처리 금지** | **처리 금지** | **검출·반환** |

entity는 **MS4_RULE_01~06**만. 입력 형식·I/O 오류를 entity에서 잡지 않는다.

### SSOT

- `MagicConstant` (34) · 격자 크기(4) · 값 범위(1~16) 단일 정의
- `34` / `16` 리터럴 산재 **금지**

---

## RED (5~7단계)

1. **선언** — Phase=RED, Layer, Track, 대상 Test ID (`reference.md` 확인).
2. **범위 고정** — PRD T01~T05 · SC 매핑 1개만 선택. 다른 Layer 코드 작성 금지.
3. **테스트 작성** — `test_d_*` 또는 `test_u_*`에 `D-*` / `U-*` docstring·함수명 반영.
4. **Mock 규칙** — Logic: 실제 domain fixture만. UI: I/O Mock만 (control Mock 허용).
5. **assert** — 기대값 명시. `skip` · `xfail` · assert 완화 **금지**.
6. **실행** — 아래 Test Loop RED 명령. **FAIL 확인** (ImportError·AssertionError = 정상 RED).
7. **보고** — 실패 메시지·원인 1줄. **구현 코드 아직 작성하지 않음.**

---

## GREEN (5~7단계)

1. **선언** — Phase=GREEN, Layer, Track, Test ID.
2. **최소 구현** — 해당 Layer에만 코드 추가. 역방향·횡단 import 금지.
3. **SSOT** — 상수는 `MagicConstant`(등)에서만. 리터럴 34/16 추가 금지.
4. **오류 경계** — E001~E005를 entity에 넣지 않음. boundary/control 역할 유지.
5. **실행** — 대상 테스트 1개 → 해당 Layer 디렉터리 순으로 pytest.
6. **확장 금지** — RED 범위 밖 기능·리팩터·다른 Test ID 동시 Green 금지.
7. **보고** — pytest 통과 로그. 변경 파일 목록.

---

## REFACTOR (5~7단계)

1. **선언** — Phase=REFACTOR, Layer, Track.
2. **전제** — 대상 Track 테스트가 이미 전부 Green.
3. **범위** — 동일 Layer 내부 정리만 (이름·중복·private 추출). 공개 API 변경 시 테스트 먼저.
4. **금지** — assert 완화 · skip · xfail · cross-layer 이동 · Domain Mock 도입.
5. **실행** — Layer 디렉터리 pytest → Track 전체 pytest.
6. **ECB 검증** — `entity`가 외부 import 없는지 확인.
7. **보고** — 리팩터 요약 + pytest still green.

---

## Test / Review Loop

| 시점 | 명령 | 기대 |
|---|---|---|
| RED 직후 | `pytest tests/<layer>/test_d_<name>.py -q` (또는 `test_u_*`) | **FAIL** |
| GREEN 직후 | 동일 파일 `-q` | **PASS** |
| GREEN 확인 | `pytest tests/<layer>/ -q` | **PASS** (해당 Layer) |
| Logic Track 완료 | `pytest tests/entity/ tests/control/ -q` | **PASS** |
| UI Track 완료 | `pytest tests/boundary/ -q` | **PASS** |
| REFACTOR 후 | 위 Layer + Track 명령 재실행 | **PASS** |
| **Review (작업 종료 전)** | `pytest -q` | **PASS** (전체; 0 skip) |

Layer 경로: `entity` · `control` · `boundary`.

설치 (최초 1회): `pip install -e ".[dev]"`

**Review Loop 규칙**

- `pytest -q` exit 0 아니면 완료 보고 금지.
- `no tests ran`은 Harness만 있을 때 허용; 테스트 추가 후에는 해당 ID pytest 필수.
- 실패 시 GREEN/REFACTOR로 되돌아가 수정. assert 완화로 통과시키지 않음.

---

## 완료 보고 항목

작업 턴·세션 종료 시 아래를 포함한다.

```markdown
## TDD 완료 보고
- Phase / Layer / Track:
- Test ID: D-XX (또는 U-XX)
- PRD 매핑: T0X / SC-X
- pytest: `<실행한 명령>` → PASS | FAIL
- 변경 파일:
- ECB: entity 외부 import 없음 ✓/✗
- Mock: Logic Domain Mock 없음 ✓/✗
- E001~E007: entity 미처리 ✓/✗
- 다음: (다음 Test ID 또는 Phase)
```

git commit · push는 **사용자 요청 시만**.

---

## 추가 참고

- Logic 테스트 ID 목록: [reference.md](reference.md)
- 도메인·Rule: `docs/PRD.md` §5~8
- 프로젝트 규칙: `.cursorrules`
