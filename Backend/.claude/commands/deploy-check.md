---
description: Pre-deployment checklist — verifies tests, debug statements, and migrations
allowed-tools: Bash, Read, Grep
---
Run a pre-deployment checklist for the energycorp project:

1. **Tests**: Run `!cd Backend && python3 src/manage.py test` — report pass/fail
2. **Debug statements**: Search for `print(` in all Python files under Backend/src/ (exclude migrations and manage.py). Search for `console.log(` in all JS/JSX files under Frontend/src/.
3. **Environment files**: Check if any `.env` files exist that might be accidentally committed
4. **Migrations**: Run `!cd Backend && python3 src/manage.py showmigrations` — check for unapplied migrations

Present results as a checklist:
- [x] for passing checks
- [ ] for failing checks with details on what needs fixing