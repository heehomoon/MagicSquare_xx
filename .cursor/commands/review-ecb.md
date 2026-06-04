# Review ECB — 계약 위반 검사

MagicSquare_xx **ECB · 도메인 계약** 리뷰 전용. **코드 수정 금지** — 위반 목록만 표로 보고한다.

---

## 필수 선언

응답 **첫 줄**:

```
Phase: review | Scope: ECB·계약 | Mode: read-only
```

---

## 절차

1. **범위 읽기** — `src/{entity,control,boundary}/`, `tests/{entity,control,boundary}/` (사용자 지정 파일 우선).
2. **체크 5항** — 아래 검사표 기준으로 파일·라인 단위 확인.
3. **위반만 기록** — Pass 항목은 `✓` 한 줄 요약. 위반은 표에 **파일:라인 · 근거 · 심각도**.
4. **수정 금지** — 제안은 "권고" 열에만. `src/` · `tests/` 편집·커밋하지 않음.

---

## 검사표 (체크 5항)

| # | 체크 | Pass 기준 | 위반 예 |
|---|---|---|---|
| **R1** | **import 방향** | `boundary → control → entity`만. entity는 **외부 계층 import 없음**. control은 entity만. boundary는 control(·entity DTO 변환). 역방향·횡단 금지 | `entity`가 `control`/`boundary` import · control→boundary |
| **R2** | **entity · E001~E005** | entity에 E001~E005 처리·raise·분기 **없음**. MS4_RULE_01~06(도메인)만 | entity에서 `E001` 문자열·입력 형식 검증 |
| **R3** | **int[6] · 1-index** | 출력 `[r1,c1,n1,r2,c2,n2]` 좌표 **1-index** (0-index 금지). 길이 6 | `grid[0][0]`을 출력 좌표로 그대로 반환 · len≠6 |
| **R4** | **MagicConstant SSOT** | `34`/`16`/격자 크기 `4`는 **MagicConstant(등) 단일 정의**에서만. 산재 리터럴 없음 | entity·control·test에 `34` 하드코딩 (SSOT 제외) |
| **R5** | **Logic Track · Domain Mock** | `tests/entity/`, `tests/control/`(`test_d_*`)에서 Grid·Axis·Rule **Mock/stub/fake 금지** | `@patch("...Grid")` · MagicMock으로 Rule 대체 |

**참고 (리뷰 범위 밖이나 언급 가능):** E006~E007는 boundary 전용 · UI Track I/O Mock은 허용.

---

## 산출 형식

```markdown
## ECB · 계약 리뷰

| ID | 결과 | 파일:라인 | 내용 | 권고 |
|---|---|---|---|---|
| R1 | PASS / FAIL | — 또는 path:L | 위반 설명 | (FAIL만) |
| R2 | … | | | |
| R3 | … | | | |
| R4 | … | | | |
| R5 | … | | | |

**요약:** FAIL n건 · BLOCKER n건
**조치:** (수정은 사용자/GREEN·REFACTOR 요청 후)
```

**심각도:** BLOCKER = R1/R2/R5 · MAJOR = R3/R4

---

## 탐색 힌트 (읽기 전용)

```bash
# import 방향 (entity가 상위 import하는지)
rg "^from (control|boundary)|^import (control|boundary)" src/entity/

# E001~E005 in entity
rg "E00[1-5]" src/entity/

# 리터럴 34/16 (MagicConstant 정의 파일 제외하고 육안 확인)
rg "\b34\b|\b16\b" src/ tests/

# Domain Mock in Logic tests
rg "Mock|patch|MagicMock|fake_" tests/entity/ tests/control/
```

---

## 금지

- `src/` · `tests/` **수정·생성·삭제**
- pytest 실행으로 "고치기" · assert 완화 제안
- git commit · push (사용자 요청 없이)
- 스타일·네이밍·성능 등 **계약 외** 리뷰 (별도 요청 시만)

계약 기준: `.cursorrules` · `docs/PRD.md` · `.cursor/skills/magic-square-tdd/SKILL.md`
