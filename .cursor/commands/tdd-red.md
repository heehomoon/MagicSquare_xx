# TDD RED — 실패 테스트 먼저

MagicSquare_xx Dual-Track TDD **RED 단계만**. 구현(`src/`)은 작성하지 않는다.

---

## 필수 선언

응답 **첫 줄**에 반드시 선언한다 (한국어 본문 가능):

```
Phase: red | Layer: entity | control | boundary | Track: Logic | UI | Test: D-XX | U-XX
```

예:

```
Phase: red | Layer: entity | Track: Logic | Test: D-01
```

---

## 절차

1. **ID 확인** — `.cursor/skills/magic-square-tdd/reference.md`에서 `D-*` / PRD T01~T05 매핑 확인. UI Track이면 `U-*` 명시.
2. **파일 결정** — Logic: `tests/{entity,control}/test_d_*.py` · UI: `tests/boundary/test_u_*.py`. 한 사이클 = **Test ID 1개**.
3. **AAA 테스트 작성**
   - **Arrange** — Logic: 실제 격자 fixture (`int[4][4]`, 빈칸 2, 1~16). UI: I/O Mock만 (stdin·파일·CLI).
   - **Act** — 테스트 대상 호출 (아직 없으면 import → ImportError도 RED로 인정).
   - **Assert** — 기대값 명시 (pass/fail·축·index·actual sum·E00X 등).
4. **Mock 규칙** — Logic Track: Grid·Axis·Rule **Domain Mock 금지**. UI Track: control Mock 허용, I/O Mock 허용.
5. **pytest 실행** — 대상 파일 1개. **FAIL 확인** (AssertionError · ImportError = 정상 RED).
6. **보고** — 아래 보고 형식. `src/` 미변경 확인.

---

## pytest 예시 (bash)

```bash
# Logic — entity
pytest tests/entity/test_d_magic_constant.py -q

# Logic — control
pytest tests/control/test_d_validate_grid.py -q

# UI — boundary
pytest tests/boundary/test_u_cli_validate.py -q

# 상세 traceback (RED 디버그)
pytest tests/entity/test_d_01_complete_grid.py -v
```

기대: exit code **≠ 0** (FAIL). exit 0이면 RED 미달 — assert 또는 대상 미구현 여부 재확인.

---

## 보고

```markdown
## RED 완료
- Test ID: D-XX (T0X / SC-X)
- pytest: `pytest tests/.../test_d_....py -q` → FAIL
- FAIL 요약: (한 줄, e.g. ImportError: MagicConstant / AssertionError: ok expected True)
- 변경 파일: tests/entity/test_d_....py (tests/만)
- src/ 변경: 없음 ✓
```

---

## 금지

- `src/` **어떤 파일도** 수정·생성·삭제
- Logic Track에서 Grid · Axis · Rule **Domain Mock**
- `pytest.skip` · `pytest.mark.xfail` · assert 완화·삭제
- 한 RED에 Test ID 2개 이상 동시 추가
- GREEN · REFACTOR 코드 선행 작성

다음 단계: `/tdd-green` (또는 사용자 GREEN 요청).
