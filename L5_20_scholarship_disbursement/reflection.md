# Reflection — Lab 5: Static Code Analysis

**Student:** Manoj PS | PES1UG24CS265 | Section E

**1. Which issues were the easiest and hardest to fix?**
Easiest: style issues (`== None`, docstrings, line length) and the mutable default, which are mechanical one-line fixes. Hardest: removing the `global` total, since the state had to move somewhere else; I computed it from the database with a `SUM` query. The SQL injection fix was also important but simple once I used `?` placeholders.

**2. Did the tools report any false positives?**
Not really. The `os.system("echo ...")` warnings (B605/B607) are low severity since the command is a constant string, so the real risk here is small, but the pattern is unsafe if the string ever includes user input, so removing it was still right. Pylint's `disbursed_total` naming warning was a side effect of using a global rather than a real problem on its own.

**3. How could these tools be integrated into your workflow?**
Run Flake8 and Pylint as a pre-commit hook and Bandit plus Pylint in CI (e.g. GitHub Actions) so a pull request fails if the Pylint score drops below a threshold or Bandit finds medium/high issues. Editors can also show Flake8/Pylint warnings live while typing.

**4. What tangible improvements did you see in the code?**
Pylint went from 5.00 to 10.00, Bandit from 4 findings (1 medium) to 0, and Flake8 from 6 warnings to 0. Beyond the numbers: the code is no longer injectable, no longer shares state between calls through `audit=[]`, no longer silently swallows errors, is readable with docstrings and PEP 8 formatting, and can be imported without side effects. Behavior and output are unchanged.
