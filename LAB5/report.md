# Lab 5 Report: Static Code Analysis (Food Delivery Order Queue Manager)

**File analysed:** `delivery_system.py` (repo L5_05_food_delivery)

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 6.27/10 (22 messages) | 10.00/10 |
| Bandit | 3 issues (1 Medium, 2 Low) | 0 |
| Flake8 | 12 issues | 0 |

## Commits (one per tool)

1. `Fix Bandit findings`: pickle replaced with JSON; `try/except/pass` removed and replaced with explicit validation.
2. `Fix Flake8 findings`: PEP 8 blank lines and line wrapping.
3. `Fix Pylint findings`: `OrderQueue` class (no globals), docstrings, naming, `with` blocks, encodings, narrow exceptions, no mutable default, input validation, `__main__` guard.

A baseline commit holds the original code and the "before" reports.

## Behaviour changes

Original run: Ravi's order totalled 249 (unknown "sushi" charged 99), "teleported" was stored as a status, order 42 and the empty order were handled silently. Now: invalid orders are rejected, bad statuses/ids are reported, revenue still equals 290 for the valid delivered order, and the backup/restore cycle still works (as JSON).

## Deliverables

- `delivery_system.py` (updated), `issues.md`, `reflection.md`, this report
- `reports/before/` (pylint, bandit, flake8 reports before fixes)
- `reports/after/` (pylint, bandit, flake8 reports after fixes)
- Git history: 4 commits (baseline + 3 fix commits)
