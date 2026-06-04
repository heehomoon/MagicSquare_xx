# MagicSquare — Product Requirements Document (PRD)

**버전:** 0.1 (초안)  
**일자:** 2026-06-04  
**프로젝트:** MagicSquare_1004  
**근거:** `Report/01.MagicSquare_ProblemDefinition_Report.md`

---

## 1. 개요

### 1.1 배경

4×4 부분 마방진 학습자가 **10선(행4+열4+대각2, 합 34)** 을 맞출 때, 대각선 검증을 빠뜨린 채 진행하다 **늦게** 오류를 발견하고 **약 20분**을 재작업에 사용한다 (Mom Test 증거).

### 1.2 제품 목적

학습자가 채운 4×4 격자에 대해 **10선 조건을 즉시 판정**하고, **어느 축이 틀렸는지** 알려 **판정 지연·재작업 시간**을 줄인다.

### 1.3 한 줄 정의

**4×4 부분 마방진(빈칸 2, 1~16, 10선 합 34) 조건 판정기**

---

## 2. 사용자

### 2.1 Primary Persona

- 4×4 격자, **빈칸 2개(0)**, **1~16**, **10선 합 34** 맞추는 **학습자**
- 과제·연습에서 **손으로** 빈칸을 채운 뒤 스스로 또는 도구로 검증

### 2.2 사용자 스토리 (초안)

1. **학습자**로서, 빈칸 2개를 채운 4×4 격자를 입력하면, **10선이 합 34인지** 바로 알고 싶다 — **대각선을 빼먹고 20분 낭비하지 않기 위해**.
2. **학습자**로서, 틀렸을 때 **어느 행/열/대각선**이 문제인지 알고 싶다 — **무엇을 다시 맞출지** 바로 알기 위해.

---

## 3. 문제 정의

### 3.1 진짜 문제

4×4 부분 마방진(**빈칸 2, 1~16, 10선 합 34**)을 손으로 채울 때, **행4·열4**는 맞춰도 **대각선 2선** 중 하나를 검증하지 않은 채 진행하다가 늦게야 틀림을 알게 되어, **과제에서 20분 가까이** 다시 맞추는 데 쓴다.

### 3.2 해결 방향 (최소)

| 포함 | 제외 |
|---|---|
| 10선(합 34) **판정** | 빈칸 **자동 채우기** |
| 실패 **축 식별** | 풀이 생성·힌트 UI |
| 4×4·1~16·빈칸 2 맥락 | 3×3 / 5×5 일반화 (v0.1) |

---

## 4. 목표 및 성공 기준

### 4.1 제품 목표

| ID | Goal |
|---|---|
| **G-1** | 채우기 직후 **수 초 내** 10축 판정 |
| **G-2** | **대각선-only fail** 케이스 탐지 (행·열 OK) |
| **G-3** | fail 시 **축 종류 + 인덱스 + 실제 합** 제공 |

### 4.2 성공 기준 (Mom Test 연결)

| ID | Acceptance Criteria | Mom Test |
|---|---|---|
| **SC-1** | 4×4, 빈칸 2, 1~16 격자 → 전 축 결과 **즉시** 반환 | “지난주 OO 과제에서” |
| **SC-2** | **10축** 모두 검사; 34≠ 축 있으면 `ok: false` | “행·열·대각선 합 맞췄는데” |
| **SC-3** | 행·열 pass, 대각선 1개 fail → **주/부 대각선 구분** | “대각선 하나를 빼먹어서 20분” |

---

## 5. 도메인 규칙 (Rule)

| ID | 규칙 |
|---|---|
| **MS4_RULE_01** | 격자는 **4×4** |
| **MS4_RULE_02** | 허용 값: `0`(빈칸), `1~16` — 0 제외 숫자는 **각 1회**, 중복 불가 |
| **MS4_RULE_03** | 마방 상수 **MAGIC = 34** |
| **MS4_RULE_04** | 검증 축: **행 4 + 열 4 + 주대각선 1 + 부대각선 1 = 10축** |
| **MS4_RULE_05** | 축에 빈칸(0) 포함 시 해당 축 **미완** (`incomplete`) — v0.1 정책: 전체 `ok`는 **모든 축 complete & pass** |
| **MS4_RULE_06** | fail/incomplete 시 반환: **축 종류** (`row`/`col`/`diag`) + **인덱스** + **actual sum** |

### 5.1 10축 인덱스 (초안)

| 축 종류 | 인덱스 | 범위 |
|---|---|---|
| `row` | 0~3 | `grid[i][0..3]` |
| `col` | 0~3 | `grid[0..3][j]` |
| `diag` | 0 | 주대각선 `(0,0)~(3,3)` |
| `diag` | 1 | 부대각선 `(0,3)~(3,0)` |

---

## 6. 기능 요구사항 (Command)

### 6.1 `validate_grid(grid: int[4][4])`

**설명:** 4×4 격자 전체에 대해 Rule MS4_RULE_01~06 적용.

**Response (JSON 형태 초안):**

```json
{
  "ok": false,
  "magic": 34,
  "results": [
    {
      "axis": "row",
      "index": 0,
      "expected": 34,
      "actual": 34,
      "status": "pass"
    },
    {
      "axis": "diag",
      "index": 1,
      "expected": 34,
      "actual": 30,
      "status": "fail"
    }
  ],
  "violations": []
}
```

| 필드 | 설명 |
|---|---|
| `ok` | 모든 축 `pass` && Rule 02 만족 |
| `magic` | 항상 34 |
| `results` | 10축 + (선택) Rule 02 위반 |
| `violations` | `fail` 또는 `incomplete` 축 목록 |

### 6.2 `sum_axis(grid, axis_type, index)`

단일 축 합산 및 pass/fail. `axis_type` ∈ `{row, col, diag}`.

### 6.3 `find_violations(grid)`

`results` 중 `status != pass` 목록만 반환. **SC-3** — 대각선 `index` 0/1 구분 필수.

### 6.4 CLI (선택, v0.1)

```
python -m magicsquare validate --file grid.txt
```

- 입력: 4행×4열 정수 (공백/쉼표 구분)
- 출력: stdout JSON 또는 human-readable 요약

---

## 7. 비기능 요구사항

| ID | 요구 |
|---|---|
| **NFR-1** | 단일 격자 판정 **< 1초** (로컬, SC-1) |
| **NFR-2** | 외부 API·DB **불필요** (로컬 라이브러리/CLI) |
| **NFR-3** | Python 3.10+ (초안) |

---

## 8. 테스트 요구사항 (Test Loop)

| ID | 시나리오 | 기대 | SC |
|---|---|---|---|
| **T01** | 완성 4×4 마방진 (1~16) | 10축 pass, `ok: true` | SC-2 |
| **T02** | 행·열 34, **주대각선 ≠ 34** | fail, `diag index=0` | **SC-3** |
| **T03** | 빈칸 2(0), 나머지 유효 | incomplete 축 명시 | SC-1 |
| **T04** | 1~16 중복 | Rule 02 fail | — |
| **T05** | 한 행만 ≠ 34 | fail, `row index` | SC-2 |

**완료 정의 (v0.1):**

- [ ] MS4_RULE_01~06 구현
- [ ] `validate_grid`, `find_violations` 동작
- [ ] T01~T03 Green
- [ ] T02 Green (**SC-3**)

---

## 9. 범위 (Scope)

### 9.1 In Scope (v0.1)

- Rule · Command · Test Loop
- (Skill) 판정 모듈 **인터페이스 스텁** — docstring + 위임만

### 9.2 Out of Scope (v0.1)

- PyQt / 웹 UI
- 마방진 **생성·풀이** 알고리즘
- 3×3 / 5×5
- 사용자 계정·클라우드

---

## 10. 마일스톤 (초안)

| 단계 | 산출 |
|---|---|
| **M0** | Problem Definition Report ✅ |
| **M1** | Rule + `validate_grid` + T01~T03 |
| **M2** | T02 (SC-3) + `find_violations` |
| **M3** | (선택) CLI · OO 과제 격자 스팟 테스트 |

---

## 11. 리스크 및 미확인 사항

| 리스크 | 완화 |
|---|---|
| Q2 미응답 — “늦게”의 **발견 시점** 불명 | Mom Test Q2 재인터뷰 |
| 증거 2 “맞췄는데” vs 실제 대각선 오류 | T02로 **재현**; UX는 “10선 전부 표시” |
| 빈칸 포함 축 **미완** 정책 | MS4_RULE_05 문서·테스트로 고정 |

---

## 12. 참고

- `Report/01.MagicSquare_ProblemDefinition_Report.md`
- `Report/01. MagicSquare_1004_MomTest_Report.md`
- `Report/03. MagicSquare_1004_Session3_Workbook.md`
