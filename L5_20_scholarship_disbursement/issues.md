# Issues Found — scholarship_disbursement.py

**Student:** Manoj PS | PES1UG24CS265 | Section E

Scores: Pylint **5.00 → 10.00** | Bandit **4 issues → 0** | Flake8 **6 issues → 0**

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| SQL injection (B608) | Security (Medium) | 10 | `INSERT` query built with `%` string formatting from `student`/`scheme`; a name like `x'); DROP TABLE awards;--` alters the query | Parameterized query with `?` placeholders and a values tuple |
| `os.system` shell call (B605, B607) | Security (Low) | 26 | Spawns a shell with a partial executable path just to echo a string | Removed the shell call, replaced with `print()` (no `os` import needed) |
| try/except/pass (B110) + broad `except Exception` (W0718) | Security / Bug | 25-28 | Swallows every error silently, hiding failures | Removed the block; nothing in it can fail now |
| Mutable default argument (W0102) | Bug | 9 | `audit=[]` is created once and shared across all calls, so the list grows between unrelated calls | Default to `None`, create a new list inside the function |
| Global statement (W0603) | Design | 16 | `disbursed_total` mutated via `global`; state can drift from the database | Removed global; total is computed from the DB by `get_disbursed_total()` |
| Inconsistent return (R1710) | Bug / Style | 15-21 | `disburse` returns a value in one branch and implicitly `None` in the other | Added explicit `return None` |
| `== None` (C0121 / E711) | Style | 32 | Equality comparison with `None` | Changed to `is None` |
| Naming (C0103) | Style | 6, 31 | `bySchemeCount` is camelCase; `disbursed_total` is not UPPER_CASE as a module constant | Renamed to `by_scheme_count`; global removed |
| Missing docstrings (C0114, C0116) | Style | 1, 9, 15, 24, 31, 37 | No module or function docstrings | Added concise docstrings |
| Line too long (E501 / C0301) | Style | 5, 10, 17, 19, 34 | Lines over 79 chars | Wrapped SQL strings and calls |
| Code runs on import | Design | 45 | `main()` called at module level, runs on import | Added `if __name__ == "__main__":` guard |

Program output is identical before and after:
```
50000 None
1 50000
archiving awards
```
