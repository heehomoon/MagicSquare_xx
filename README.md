# MagicSquare

4×4 **부분 마방진** 조건 판정기 — Mom Test로 검증한 학습자 문제를 **10선(합 34)** 판정으로 해결합니다.

| | |
|---|---|
| **프로젝트 코드** | MagicSquare_1004 |
| **버전** | v0.1 (초안) |
| **상태** | Harness 완료 · **M1 RED 진행 중** |
| **언어 (계획)** | Python 3.10+ |

---

## 한 줄 정의

> **4×4 부분 마방진(빈칸 2, 1~16, 10선 합 34) 조건 판정기**

채운 직후 **10선**을 빠짐없이 검사하고, 틀린 **행 / 열 / 대각선**을 알려 **판정 지연·재작업 시간**을 줄입니다.  
풀이 생성·자동 채우기·UI는 v0.1 범위 **밖**입니다.

---

## 배경 (Mom Test)

**페르소나:** 4×4 격자, 빈칸 2개(`0`), 1~16, **10선(행4+열4+대각2) 합 34** 맞추는 학습자

**진짜 문제:**

4×4 부분 마방진(**빈칸 2, 1~16, 10선 합 34**)을 손으로 채울 때, **행4·열4**는 맞춰도 **대각선 2선** 중 하나를 검증하지 않은 채 진행하다가 늦게야 틀림을 알게 되어, **과제에서 20분 가까이** 다시 맞추는 데 쓴다.

| # | Mom Test 증거 (과거 사실) |
|---|---|
| 1 | “**지난주 OO 과제**에서” |
| 2 | “**빈칸 2개 넣고 행·열·대각선 합 맞췄는데**” |
| 3 | “**대각선 하나를 빼먹어서 20분 날렸다**” |

**표면 문제 (하지 않을 정의):** “10선(합 34) **프로그램/앱**을 만든다” — 목표는 **앱**이 아니라 **늦은 판정으로 인한 20분 재작업**입니다.

---

## 도메인 규칙

| 항목 | 값 |
|---|---|
| 격자 | 4×4 |
| 빈칸 | `0` (과제 예: 2개) |
| 숫자 | 1~16 (중복 없음) |
| 마방 상수 | **MAGIC = 34** |
| 검증 축 | **10축** = 행 4 + 열 4 + 주대각선 1 + 부대각선 1 |

| Rule ID | 내용 |
|---|---|
| MS4_RULE_01 | 격자 4×4 |
| MS4_RULE_02 | 값 `0` 또는 `1~16`, 0 제외 각 1회 |
| MS4_RULE_03 | MAGIC = 34 |
| MS4_RULE_04 | 검증 축 10개 |
| MS4_RULE_05 | 축에 빈칸 있으면 `incomplete` |
| MS4_RULE_06 | fail/incomplete 시 축 종류·인덱스·실제 합 반환 |

---

## R-G-I-O

| | |
|---|---|
| **Role** | 4×4 부분 마방진 **조건 판정기** |
| **Goal** | 행·열만 OK·대각선 fail 상태를 **채우기 직후** 탐지 → 재작업 ≈20분 감소 |
| **Input** | `int[4][4]` — `0` 또는 `1~16` |
| **Output** | 10축 pass/fail + 위반 축 (`row` / `col` / `diag`, index, actual sum) |

---

## 성공 기준

| ID | 기준 | Mom Test |
|---|---|---|
| **SC-1** | 4×4·빈칸 2·1~16 → **수 초 내** 10축 판정 | “지난주 OO 과제에서” |
| **SC-2** | **10축** 전부 검사, 34≠ → fail | “행·열·대각선 합 맞췄는데” |
| **SC-3** | 행·열 OK, **대각선 1개만** fail → 주/부 구분 | “대각선 하나를 빼먹어서 20분” |

---

## 범위 (v0.1)

| In Scope | Out of Scope |
|---|---|
| Rule · Command · Test Loop | PyQt / 웹 UI |
| `validate_grid`, `find_violations` | 빈칸 자동 채우기 · 풀이 생성 |
| T01~T05 (T02 = SC-3 핵심) | 3×3 / 5×5 일반화 |

---

## 프로젝트 구조

```
MagicSquare_xx/
├── README.md
├── docs/
│   ├── PRD.md
│   └── TDD_RED_TODO.md                             # RED 단계 설계 · To Do (SSOT)
├── src/{entity,control,boundary}/
├── tests/{entity,control,boundary}/
├── Report/
│   ├── 01.MagicSquare_ProblemDefinition_Report.md
│   ├── 02.MagicSquare_Harness_Architecture_Report.md
│   ├── 03.MagicSquare_TDD_RED_Planning_Report.md
│   ├── 04.MagicSquare_D_LOC_RED_Skeleton_Report.md
│   ├── 05.MagicSquare_D_LOC_GREEN_Report.md
│   └── 01. MagicSquare_1004_MomTest_Report.md
└── Prompting/
    └── 06. MagicSquare_1004_Export_Transcript.md  # … 01~05 포함
```

---

## 문서 가이드

| 읽을 순서 | 파일 | 내용 |
|---|---|---|
| 1 | [Report/01.MagicSquare_ProblemDefinition_Report.md](Report/01.MagicSquare_ProblemDefinition_Report.md) | 문제 정의 · Mom Test · Non-Goals |
| 2 | [docs/PRD.md](docs/PRD.md) | Rule · API · Test · 마일스톤 |
| 3 | [docs/TDD_RED_TODO.md](docs/TDD_RED_TODO.md) | RED 단계 설계 · Given/Then · 우선순위 |
| 4 | [Report/02.MagicSquare_Harness_Architecture_Report.md](Report/02.MagicSquare_Harness_Architecture_Report.md) | ECB · Dual-Track · Harness |
| 5 | [Report/03.MagicSquare_TDD_RED_Planning_Report.md](Report/03.MagicSquare_TDD_RED_Planning_Report.md) | RED 설계 · D-LOC · M1 |
| 6 | [Report/04.MagicSquare_D_LOC_RED_Skeleton_Report.md](Report/04.MagicSquare_D_LOC_RED_Skeleton_Report.md) | D-LOC-01 RED · pytest |
| 7 | [Report/05.MagicSquare_D_LOC_GREEN_Report.md](Report/05.MagicSquare_D_LOC_GREEN_Report.md) | D-LOC-01 GREEN · find_blank_coords |
| 참고 | [Report/01. MagicSquare_1004_MomTest_Report.md](Report/01.%20MagicSquare_1004_MomTest_Report.md) | 원본 인터뷰 Q&A |
| 참고 | [Prompting/06. MagicSquare_1004_Export_Transcript.md](Prompting/06.%20MagicSquare_1004_Export_Transcript.md) | D-LOC GREEN Export |

---

## 계획 API

```python
validate_grid(grid: int[4][4]) -> ValidationResult
sum_axis(grid, axis_type, index) -> AxisResult
find_violations(grid) -> list[AxisResult]   # SC-3: diag index 0/1
```

**응답 예 (초안):**

```json
{
  "ok": false,
  "magic": 34,
  "results": [
    { "axis": "diag", "index": 1, "expected": 34, "actual": 30, "status": "fail" }
  ],
  "violations": []
}
```

**CLI (선택, M3):**

```bash
python -m magicsquare validate --file grid.txt
```

---

## Test Loop

| ID | 시나리오 | SC |
|---|---|---|
| T01 | 완성 4×4 마방진 (1~16) | SC-2 |
| T02 | 행·열 34, 주대각선 ≠ 34 | **SC-3** |
| T03 | 빈칸 2, 나머지 유효 | SC-1 |
| T04 | 1~16 중복 | Rule 02 |
| T05 | 한 행만 ≠ 34 | SC-2 |

**v0.1 완료 정의:** MS4_RULE_01~06 · `validate_grid` / `find_violations` · T01~T03 Green · **T02 Green**

---

## TDD RED 체크리스트

상세 설계(Given · Then · Expected RED Failure): [docs/TDD_RED_TODO.md](docs/TDD_RED_TODO.md)

**규칙:** 한 사이클 = Test ID 1개 · `src/` 변경 금지 · `pytest` **FAIL** = RED 완료

### 공통

- [ ] `pip install -e ".[dev]"` (최초 1회)
- [ ] RED 시 `src/` 미변경 확인
- [ ] `pytest.skip` · `xfail` · assert 완화 **금지**

### Boundary (UI Track · `tests/boundary/`)

입력·형식·I/O 차단. entity/control 호출 없음.

- [ ] **U-IN-01** — `grid=None` → `E003` `INVALID_NULL`
- [ ] **U-IN-02** — `grid=3×4` → `E001` `INVALID_SIZE`
- [ ] **U-IN-03** — 빈칸 `0`이 2개가 아님 → `E002` `INVALID_BLANKS`
- [ ] **U-IN-04** — 값이 `0`·`1~16` 밖 → `E004` `INVALID_VALUE`
- [ ] **U-IN-05** — 파싱 실패 → `E005` `INVALID_FORMAT`
- [ ] **U-IN-06** — 파일 없음/읽기 실패 → `E006` `IO_ERROR`
- [ ] **U-OUT-01** — 유효 입력 G1 → `int[6]` 길이 6, 좌표 1-index
- [ ] Boundary 공통: I/O Mock만 · `pytest tests/boundary/test_u_*.py -q` → FAIL

### Logic (Logic Track · `tests/entity/` · `tests/control/`)

도메인 Rule·Command. **Domain Mock 금지**, 실제 `int[4][4]` fixture만.

**우선순위:** `D-00` 선행 → `D-01` → `D-03` → `D-02` → `D-04` → `D-05`

- [ ] **D-00** — `MagicConstant == 34` (entity, SSOT)
- [ ] **D-01** — 완성 격자 G1 → `ok: true`, 10축 pass (T01 / SC-2)
- [ ] **D-03** — 빈칸 2개 → `incomplete`, `ok: false` (T03 / SC-1)
- [ ] **D-02** — 주대각 `index=0` fail (T02 / **SC-3**)
- [ ] **D-04** — 1~16 중복 → Rule 02 위반 (T04)
- [ ] **D-05** — 한 행만 합 ≠ 34 → `row` index fail (T05 / SC-2)
- [ ] Logic 공통: Domain Mock 없음 · `pytest tests/<layer>/test_d_*.py -q` → FAIL

### Logic — 흐름 (UI Track · boundary, control Mock 허용)

- [ ] **U-FLOW-01** — `grid=None` → `validate_grid()` 0회 호출
- [ ] **U-FLOW-02** — boundary 오류 → `find_violations()` 0회 호출
- [ ] 흐름 공통: `pytest tests/boundary/test_u_flow_*.py -q` → FAIL

### Fixture G1 (T01 · `D-01` · `U-OUT-01`)

```text
[[16, 3,  2, 13],
 [ 5, 10, 11,  8],
 [ 9,  6,  7, 12],
 [ 4, 15, 14,  1]]
```

---

## 마일스톤

| 단계 | 산출 | 상태 |
|---|---|---|
| **M0** | Problem Definition · PRD · README | ✅ |
| **M1** | RED (`D-*` · `U-*`) → Rule + `validate_grid` + T01~T03 Green | 🔄 |
| **M2** | T02 (SC-3) + `find_violations` | ⬜ |
| **M3** | (선택) CLI · OO 과제 격자 스팟 테스트 | ⬜ |

---

## 방법론

| 단계 | 방법 |
|---|---|
| STEP 1 | **Mom Test** (Rob Fitzpatrick) — 과거 사실 인터뷰 |
| 세션 3 | **8계층** — Rule → Command → (Skill) → Test Loop |
| 구현 | Dual-Track TDD (RED → GREEN → REFACTOR) — SC-1~3 ↔ T01~T05 · `D-*` / `U-*` |

---

## 알려진 리스크

- Mom Test **Q2 미응답** — 오류 발견 시점(제출 전 / 자가 검산 / 채점 후) 미확인
- 증거 2 “맞췄는데” vs 실제 대각선 오류 → **T02**로 재현·검증

---

## 라이선스

미정
