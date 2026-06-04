# TDD RED — To Do List

**버전:** 0.1  
**일자:** 2026-06-04  
**프로젝트:** MagicSquare_xx  
**근거:** `docs/PRD.md` · `.cursor/skills/magic-square-tdd/reference.md` · `.cursorrules`  
**상태:** M1 RED 미착수 (`tests/`에 `test_d_*` · `test_u_*` 없음)

---

## 1. 개요

Dual-Track TDD **RED 단계** 설계안을 To Do로 추적한다. 한 사이클 = **Test ID 1개**, `src/` 변경 금지.

| 구분 | Track | 테스트 ID | 대상 경로 |
|---|---|---|---|
| **Boundary** | UI | `U-IN-*`, `U-OUT-01` | `tests/boundary/test_u_*.py` |
| **Logic** | Logic | `D-*` | `tests/entity/`, `tests/control/` |
| **Logic (흐름)** | UI | `U-FLOW-*` | `tests/boundary/test_u_*.py` (control Mock 허용) |

### RED 실패 유형 (정상)

| 유형 | 의미 |
|---|---|
| `ImportError` / `ModuleNotFoundError` | `src/` 미구현 |
| `AssertionError` | 테스트·스텁만 있고 기대값 불일치 |
| `pytest.fail("RED")` | 흐름·출력 계약용 명시 RED |

### 공통 Fixture — G1 (T01 완성 격자)

PRD T01 · SC-2 · `U-OUT-01` · `D-01` 공용:

```text
[[16, 3,  2, 13],
 [ 5, 10, 11,  8],
 [ 9,  6,  7, 12],
 [ 4, 15, 14,  1]]
```

(빈칸 0개, 1~16 각 1회, 10축 합 34)

---

## 2. Boundary — To Do (UI Track)

입력·형식·I/O는 **boundary**에서 차단. entity/control **호출 0회** (흐름은 §4 `U-FLOW-*`).

| # | Test ID | Given | Then (기대값) | Expected RED Failure | Layer | 완료 |
|---|---|---|---|---|---|:---:|
| 1 | **U-IN-01** | `grid=None` (또는 미전달) | `E003` `INVALID_NULL` | `ModuleNotFoundError` 또는 `AssertionError` | boundary | ☐ |
| 2 | **U-IN-02** | `grid=3×4` (행·열 불일치) | `E001` `INVALID_SIZE` | `AssertionError` | boundary | ☐ |
| 3 | **U-IN-03** | 빈칸 `0`이 **2개가 아님** (0·1·3개+) | `E002` `INVALID_BLANKS` | `AssertionError` | boundary | ☐ |
| 4 | **U-IN-04** | 셀 값이 `0`·`1~16` 밖 (예: `17`, `-1`) | `E004` `INVALID_VALUE` | `AssertionError` | boundary | ☐ |
| 5 | **U-IN-05** | 파일/CLI 파싱 실패 (비정수·행 수 ≠4) | `E005` `INVALID_FORMAT` | `AssertionError` | boundary | ☐ |
| 6 | **U-IN-06** | `--file` 경로 없음 / 읽기 실패 | `E006` `IO_ERROR` | `AssertionError` | boundary | ☐ |
| 7 | **U-OUT-01** | 유효 입력 **G1** | `int[6]` 길이 **6**, 좌표 **1-index** `[r1,c1,n1,r2,c2,n2]` | `pytest.fail("RED")` 또는 `AssertionError` | boundary | ☐ |

### Boundary 체크리스트

- [ ] `tests/boundary/test_u_*.py` 생성 (Test ID 1개씩)
- [ ] I/O Mock만 사용 (Domain Mock 금지)
- [ ] `pytest tests/boundary/test_u_<name>.py -q` → **FAIL** 확인
- [ ] `src/` 변경 없음 확인

> E001~E007 세부 명칭: `.cursorrules` — boundary 소유, entity는 E001~E005 처리 금지.

---

## 3. Logic — To Do (Logic Track)

도메인 Rule·Command·SC 검증. **Domain Mock 금지**, 실제 `int[4][4]` fixture만 사용.

| # | Test ID | Given | Then (기대값) | Expected RED Failure | Layer | PRD | 완료 |
|---|---|---|---|---|---|---|:---:|
| 0 | **D-00** | (없음) | `MagicConstant == 34` (SSOT) | `ImportError` | entity | 선행 | ☐ |
| 1 | **D-01** | 완성 4×4 마방진 **G1** | `ok: true`, 10축 `status: "pass"` | `ImportError` → `AssertionError` | control | T01 / SC-2 | ☐ |
| 2 | **D-03** | 빈칸 **2개(0)**, 나머지 1~16 유효 | 해당 축 `incomplete`, `ok: false` | `AssertionError` | control | T03 / SC-1 | ☐ |
| 3 | **D-02** | 행·열 34, **주대각(index=0) ≠ 34** | `diag index=0` fail | `AssertionError` | control | T02 / **SC-3** | ☐ |
| 4 | **D-04** | 1~16 **중복** | Rule 02 위반, `ok: false` | `AssertionError` | entity 또는 control | T04 | ☐ |
| 5 | **D-05** | **한 행만** 합 ≠ 34 | `axis: row`, 해당 index, `actual` ≠ 34 | `AssertionError` | control | T05 / SC-2 | ☐ |

**M1 RED 우선순위:** `D-01` → `D-03` → `D-02` → `D-04` → `D-05` (`D-00` 선행)

### Logic 체크리스트

- [ ] `D-00` — `tests/entity/test_d_magic_constant.py` (예시 파일명)
- [ ] `D-01`~`D-05` — `tests/control/test_d_*.py` (Layer별 분리 가능)
- [ ] Grid·Axis·Rule **Domain Mock 없음**
- [ ] `pytest tests/<layer>/test_d_<name>.py -q` → **FAIL** 확인
- [ ] `src/` 변경 없음 확인

---

## 4. Logic (흐름) — To Do (UI Track · boundary)

boundary 오류 시 control **위임 전 차단**. control Mock **허용**.

| # | Test ID | Given | Then (기대값) | Expected RED Failure | Layer | 완료 |
|---|---|---|---|---|---|:---:|
| 1 | **U-FLOW-01** | `grid=None` (U-IN-01과 동일) | `validate_grid()` **0회** 호출 | `pytest.fail("RED")` | boundary | ☐ |
| 2 | **U-FLOW-02** | `E001`/`E002` 등 boundary 오류 입력 | `find_violations()` **0회** 호출 | `pytest.fail("RED")` | boundary | ☐ |

### 흐름 체크리스트

- [ ] `U-FLOW-01` — `U-IN-01` RED 완료 후 또는 병행 설계
- [ ] control Mock으로 호출 횟수 assert
- [ ] `pytest tests/boundary/test_u_flow_*.py -q` → **FAIL** 확인

---

## 5. 마일스톤 연계

| 순서 | Harness Report §8 | Track | 관련 To Do |
|---|---|---|---|
| 1 | `MagicConstant` · Grid entity + `D-*` RED | Logic / entity | `D-00`, entity 측 `D-04` |
| 2 | `validate_grid` control + `D-*` GREEN | Logic / control | `D-01`~`D-05` (RED 후 GREEN) |
| 3 | T02 SC-3 · `find_violations` | Logic / control | `D-02` |
| 4 | boundary · E001~E007 + `U-*` | UI / boundary | §2 · §4 전체 |

**v0.1 완료 정의:** MS4_RULE_01~06 · T01~T03 Green · **T02 Green (SC-3)** — `docs/PRD.md` §8

---

## 6. 참고

| 문서 | 내용 |
|---|---|
| `docs/PRD.md` | Rule · Command · Test Loop T01~T05 |
| `.cursor/skills/magic-square-tdd/reference.md` | `D-*` ID · PRD 매핑 |
| `.cursor/skills/magic-square-tdd/SKILL.md` | RED/GREEN/REFACTOR 절차 |
| `.cursor/commands/tdd-red.md` | RED Command · pytest 예시 |
| `Report/02.MagicSquare_Harness_Architecture_Report.md` | ECB · Dual-Track · M1 순서 |

---

## 7. 진행 기록 (수동 갱신)

| 일자 | Test ID | pytest 명령 | 결과 | 비고 |
|---|---|---|---|---|
| | | | | |
