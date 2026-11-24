# Issues found in `delivery_system.py`

Tools: Pylint (6.27/10 before), Bandit (1 Medium, 2 Low), Flake8 (12 findings). Ordered high/medium severity first. Reports: `reports/before/` and `reports/after/`.

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 1 | Insecure deserialization with `pickle.load` (B301, B403) | Security (Medium/Low) | 2, 49 | `restore_orders` unpickles a file; a tampered `orders.pkl` can execute arbitrary code. | Replaced pickle with JSON (`json.dump`/`json.load`); convert order-id keys back to `int` on restore. |
| 2 | Silent failure: bare `except: pass` (B110, E722, W0702) | Bug / Security (Low) | 23-25 | `update_order_status` swallows every error (unknown id, any status), hiding bad input and even `KeyboardInterrupt`. | Explicit checks for unknown id and invalid status; print a message and return `False`/`True`. |
| 3 | Invalid status accepted (logic bug, not tool-flagged) | Bug | 21-25 | Status `"teleported"` was stored although `VALID_STATUSES` exists and was never used. | Validate against `VALID_STATUSES` before updating. |
| 4 | Unknown dishes silently cost 99 (logic bug, not tool-flagged) | Bug | 15 | `menu.get(i, 99)` charged 99 for "sushi", giving Ravi a total of 249. | Reject orders containing items not on the menu with `ValueError`. |
| 5 | Empty/anonymous order accepted (logic bug, not tool-flagged) | Bug | 29-31 | An order with no customer and no items was created and counted as delivered. | Require a non-blank customer and at least one item. |
| 6 | Mutable default argument `order_history=[]` (W0102) | Bug | 11 | The list is shared across calls; the "history" leaks between callers. | Removed the parameter; order ids tracked in the queue object. |
| 7 | Overly broad `except Exception` and file handle leak (W0718, R1732, W1514) | Quality | 28-33, 43, 49 | Any error (even a bug) loads the default menu; files opened without `with`/encoding, leaking handles on error. | Catch `OSError`/`JSONDecodeError` only; use `with open(..., encoding="utf-8")` everywhere. |
| 8 | Global mutable state (W0603, C0103 `next_id`) | Design | 5-8, 12, 28, 48 | `global orders/menu/next_id` makes code hard to test and reuse. | Wrapped state in an `OrderQueue` class. |
| 9 | Style: blank lines and long lines (E302 x7, E305, E501 x2) | Style | 11-70 | Missing blank lines between definitions; lines of 80 and 96 characters. | Reformatted to PEP 8 (2 blank lines, wrapped long lines). |
| 10 | Missing docstrings, `printQueue` naming, `%` formatting (C0114, C0116, C0103, C0209) | Style | 1-60 | No docstrings; camelCase function name; old-style string format. | Added docstrings, renamed to `print_queue`, used f-strings. |
| 11 | `main()` runs on import | Design | 70 | Importing the module executes the demo and writes a file. | Added `if __name__ == "__main__":` guard. |

**Result:** Bandit 0 issues, Flake8 0 issues, Pylint 10.00/10. All 11 documented issues fixed (minimum was 4).
