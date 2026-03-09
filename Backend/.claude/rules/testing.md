# Testing Conventions

- All new endpoints must have at least one test covering the success case
- Test names follow the pattern: `test_<action>_<condition>_<expected>`
- Example: `test_login_valid_credentials_returns_token`
- Use Django's `TestCase` for database tests, `SimpleTestCase` for pure logic
- Always test permission enforcement: verify unauthorized users get 403
- Run tests from Backend/ directory: `python src/manage.py test`