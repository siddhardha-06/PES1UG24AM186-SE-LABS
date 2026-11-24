# Reflection

*The handout text did not include the four reflection questions, so these answer the standard Lab 5 reflection topics. Replace the headings with the exact wording from your handout if it differs.*

**1. Which issues were easiest and hardest to fix?**
Flake8 issues were easiest: purely mechanical formatting. Hardest were the design-level ones (global state, silent `except: pass`, pickle), because fixing them changed behaviour and structure: the replacement needed an error-reporting strategy and a JSON round trip (JSON keys become strings, so ids must be converted back to `int`).

**2. Did the tools report any false positives, or miss real problems?**
No true false positives, but Bandit's B403 on `import pickle` is just a warning about the module. More importantly, the tools missed real bugs: unknown dishes costing 99, invalid statuses such as "teleported" being accepted, and empty orders being created. These only showed up by running the program and reading output that looked wrong.

**3. How would you integrate static analysis into a development workflow?**
Run Flake8 and Pylint as pre-commit hooks, and run all three tools (plus tests) in CI on every pull request, failing the build on any Bandit finding or a Pylint score below a threshold (e.g. 9.5). Fix issues in small commits per tool so history stays reviewable.

**4. What did you learn about code quality and security?**
Small habits (bare excepts, mutable defaults, unclosed files, pickle) cause the most serious problems, and each is cheap to avoid. Static analysis is a fast first filter, but it complements, not replaces, running the code and writing tests.
