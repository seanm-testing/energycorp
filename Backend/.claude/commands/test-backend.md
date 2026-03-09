---
description: Run Django backend tests and summarize results
allowed-tools: Bash, Read
---
Run the Django test suite with `!cd Backend/src && python3 manage.py test`.

Report:
1. Total tests run
2. Pass/fail count
3. If any failures, show the test name, file, and error message
4. Suggest a fix for each failure