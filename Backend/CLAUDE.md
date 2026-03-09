# Backend CLAUDE.md

Backend for the Energy Corporation Management System — a Django 3.0.3 REST API with DRF, token auth, and role-based permissions.

## Build & Run Commands

```bash
# From Backend/ directory
# Note: use python3 (not python) — python is not available on this system
python3 -m pip install -r requirements.txt   # Install dependencies (or: pipenv install)
python3 src/manage.py runserver              # Start dev server
python3 src/manage.py test                   # Run all tests
python3 src/manage.py test users             # Run tests for a single app
python3 src/manage.py makemigrations         # Create migrations
python3 src/manage.py migrate                # Apply migrations
python3 src/manage.py createsuperuser        # Create admin user

# Coverage (requires: pip install coverage)
cd src && python3 -m coverage run --source='.' manage.py test && python3 -m coverage report
```

## Post-Edit Checks

After editing any `models.py`, `views.py`, or `serializers.py` file in the Backend, run the `django-check` skill to validate the changes and output the report for me to view at the end of your response.

## Architecture

Settings in `src/rest/settings.py`. Root URL conf in `src/rest/urls.py`. Python 3.6.

### Django Apps and API Prefixes

| App | API Prefix | Purpose |
|-----|-----------|---------|
| `users` | `/api/user/` | Custom user model (`CustomUser`), client/worker profiles, login endpoint |
| `energytransfers` | `/api/energytransfers/` | Substations, transformers, counters, consumption history |
| `contract` | `/api/invoice/` | Contracts linking clients to counters, invoice generation/PDF/email |
| `payments` | `/api/pay/` | Direct and bank payments against invoices |
| `bancks` | `/api/bancks/` | Bank records |
| `commercial` | `/api/commercial/` | Advertising/publicity |
| `reports` | `/api/reports/` | Suspension, overdue, and distribution reports |

Each app follows: `models.py` → `serializers.py` → `views.py` → `urls.py`.

### API View Patterns

Most apps use **DRF generic views** (not ViewSets):
- `ListCreateAPIView` — List + Create
- `RetrieveAPIView` — Detail retrieval
- `ListAPIView` — List only
- `UpdateAPIView` — Update
- `DestroyAPIView` — Delete

**Exception:** `reports` uses `django.views.generic.View` + `HttpResponse(json.dumps(...))`, not DRF. Its tests use `django.test.Client` with `json.loads()`.

### Auth & Permissions

- **Auth model:** Custom `CustomUser` with email-based authentication (`AUTH_USER_MODEL = 'users.CustomUser'`)
- **Token auth:** `rest_framework.authtoken` — login returns a token + user type
- **Role-based permissions** (defined in each app's `permissions.py`):
  - Type 1 = Admin (`AllowAdmin`)
  - Type 2 = Manager (`AllowManager`)
  - Type 3 = Operator (`AllowOperator`)
- Each permission class checks `Worker.objects.filter(user=request.user.id).values('user_type')`

### Key Model Relationships

```
Substation → has many Transformator → has many Counter → has History records
Client (→ CustomUser) → Contract (links client to counter) → Invoice → Payment
Worker (→ CustomUser) has user_type field (1/2/3) for role permissions
```

## Dependencies

```
Django==3.0.3
djangorestframework==3.11.0
django-cors-headers==3.2.1
weasyprint==51                 # PDF generation for invoices
dj-database-url~=0.5.0        # PostgreSQL URL parsing (Pipfile)
psycopg2-binary~=2.8.5        # PostgreSQL driver (Pipfile)
```

## Testing

133 tests across all apps. Run from `Backend/` directory.

| App | Tests |
|-----|-------|
| `users` | 44 |
| `energytransfers` | 34 |
| `contract` | 20 |
| `payments` | 12 |
| `bancks` | 8 |
| `commercial` | 8 |
| `reports` | 7 |

Shared factory helpers in `src/tests/helpers.py`: `create_custom_user`, `create_client`, `create_worker`, `create_substation`, `create_transformator`, `create_counter`, `create_contract`, `create_invoice`, `create_history`, `create_commercial`, `create_banck`.

## Deployment

- **Docker** on Heroku (`Dockerfile` + `heroku.yml`)
- Image: `python:3.6-stretch`, runs as non-root user `myuser`
- Database: SQLite locally, PostgreSQL on Heroku
