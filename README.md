# MagicSquare

4×4 **부분 마방진** 조건 판정기 — Mom Test로 검증한 학습자 문제를 **10선(합 34)** 판정으로 해결합니다.

| | |
|---|---|
| **프로젝트 코드** | MagicSquare_1004 |
| **버전** | v0.1 (초안) |
| **상태** | 설계 · 문서화 완료 · **구현 전** |
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
│   └── PRD.md                                      # 제품 요구사항 v0.1
├── Report/
│   ├── 01.MagicSquare_ProblemDefinition_Report.md  # 문제 정의 · Mom Test · R-G-I-O
│   ├── 01. MagicSquare_1004_MomTest_Report.md      # Mom Test STEP 1 인터뷰
│   └── 03. MagicSquare_1004_Session3_Workbook.md   # 세션 3 · Rule/Command/Test
└── Prompting/
    ├── 01. MagicSquare_1004_Export_Transcript.md   # STEP 1 대화 기록
    └── 02. MagicSquare_1004_Export_Transcript.md   # 후속 세션 대화 기록
```

---

## 문서 가이드

| 읽을 순서 | 파일 | 내용 |
|---|---|---|
| 1 | [Report/01.MagicSquare_ProblemDefinition_Report.md](Report/01.MagicSquare_ProblemDefinition_Report.md) | 문제 정의 · Mom Test · Non-Goals |
| 2 | [docs/PRD.md](docs/PRD.md) | Rule · API · Test · 마일스톤 |
| 3 | [Report/03. MagicSquare_1004_Session3_Workbook.md](Report/03.%20MagicSquare_1004_Session3_Workbook.md) | 8계층( Rule → Command → Test Loop ) |
| 참고 | [Report/01. MagicSquare_1004_MomTest_Report.md](Report/01.%20MagicSquare_1004_MomTest_Report.md) | 원본 인터뷰 Q&A |
| 참고 | [Prompting/](Prompting/) | Cursor 대화 Export |

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

## 마일스톤

| 단계 | 산출 | 상태 |
|---|---|---|
| **M0** | Problem Definition · PRD · README | ✅ |
| **M1** | Rule + `validate_grid` + T01~T03 | ⬜ |
| **M2** | T02 (SC-3) + `find_violations` | ⬜ |
| **M3** | (선택) CLI · OO 과제 격자 스팟 테스트 | ⬜ |

---

## 방법론

| 단계 | 방법 |
|---|---|
| STEP 1 | **Mom Test** (Rob Fitzpatrick) — 과거 사실 인터뷰 |
| 세션 3 | **8계층** — Rule → Command → (Skill) → Test Loop |
| 구현 | TDD — Mom Test SC-1~3 ↔ T01~T05 연결 |

---

## 알려진 리스크

- Mom Test **Q2 미응답** — 오류 발견 시점(제출 전 / 자가 검산 / 채점 후) 미확인
- 증거 2 “맞췄는데” vs 실제 대각선 오류 → **T02**로 재현·검증

---

## 라이선스

미정
