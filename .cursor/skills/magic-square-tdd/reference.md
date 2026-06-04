# D-* Logic Track 테스트 ID

PRD Test Loop (T01~T05)와 1:1 매핑. 파일: `tests/{entity,control}/test_d_*.py`

| ID | PRD | 시나리오 | SC |
|---|---|---|---|
| **D-01** | T01 | 완성 4×4 마방진 (1~16), 10축 pass | SC-2 |
| **D-02** | T02 | 행·열 34, 주대각선 ≠ 34 → `diag index=0` | **SC-3** |
| **D-03** | T03 | 빈칸 2(0), 나머지 유효 → incomplete 축 | SC-1 |
| **D-04** | T04 | 1~16 중복 → Rule 02 fail | — |
| **D-05** | T05 | 한 행만 ≠ 34 → `row index` fail | SC-2 |

**우선순위 (M1):** D-01 → D-03 → D-02 (SC-3) → D-04 → D-05
