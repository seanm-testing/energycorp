# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Energy Corporation Management System — a full-stack app for managing energy distribution, billing, contracts, and customer services. Backend is a Django REST API, frontend is a React SPA.

## Build & Run Commands

### Backend (Django)

```bash
# From Backend/ directory
pip install -r requirements.txt          # Install dependencies (or: pipenv install)
python src/manage.py runserver            # Start dev server
python src/manage.py test                 # Run all tests
python src/manage.py test users           # Run tests for a single app
python src/manage.py makemigrations       # Create migrations
python src/manage.py migrate              # Apply migrations
python src/manage.py createsuperuser      # Create admin user

# Coverage (requires: pip install coverage)
cd src && coverage run --source='.' manage.py test && coverage report
```

### Frontend (React)

```bash
# From Frontend/ directory (requires Node 12 — see Frontend/CLAUDE.md)
npm install        # Install dependencies
npm start          # Start dev server
npm run build      # Production build
npm test           # Run tests (interactive watch mode)
npm test -- --watchAll=false --coverage   # Run tests once with coverage report
```

## Architecture

### Backend (`Backend/src/`)

Django 3.0.3 + Django REST Framework. Settings in `rest/settings.py`. Uses a custom user model (`CustomUser`) with email-based authentication and token auth.

**Django apps and their API prefixes:**
- `users` (`/api/user/`) — Custom user model, client/worker profiles, login endpoint
- `energytransfers` (`/api/energytransfers/`) — Substations, transformers, counters, consumption history
- `contract` (`/api/invoice/`) — Contracts linking clients to counters, invoice generation/PDF/email
- `payments` (`/api/pay/`) — Direct and bank payments against invoices
- `bancks` (`/api/bancks/`) — Bank records
- `commercial` (`/api/commercial/`) — Advertising/publicity
- `reports` (`/api/reports/`) — Suspension, overdue, and distribution reports

**Role-based permission system** (defined in each app's `permissions.py`):
- Type 1 = Admin (`AllowAdmin`)
- Type 2 = Manager (`AllowManager`)
- Type 3 = Operator (`AllowOperator`)

Each app follows standard DRF patterns: `models.py` → `serializers.py` → `views.py` → `urls.py`.

**Testing:** 133 tests across all apps using Django `TestCase` + DRF `APIClient`. Shared factory helpers in `tests/helpers.py` (create_custom_user, create_client, create_worker, create_contract, etc.). Coverage: 88%. Note: `reports` views use `django.views.generic.View` + `HttpResponse(json.dumps(...))`, not DRF — their tests use `django.test.Client` with `json.loads()`.

Database: SQLite locally, PostgreSQL on Heroku.

### Frontend (`Frontend/src/`)

React 16 + Redux + React Router 5. Key libs: Axios (HTTP), Reactstrap (UI), Leaflet (maps), Chart.js.

**Auth flow:** Login POSTs to `/api/user/login/` which returns a token + user type. `Auth` class (`components/auth/auth.js`) stores session in localStorage. `ProtectedRoute` (`components/auth/ProtectedRoute.js`) guards routes by role.

**Role-based routing in `App.js`:**
- `/admin/*` — Admin views (user management, transformer map)
- `/operator/*` — Operator views (client management, payments)
- `/manager/*` — Manager views (reports)
- `/login`, `/getBill` — Public routes

Route definitions are split across `routes/adminRoutes.js`, `routes/operatorRoutes.js`, `routes/managerRoutes.js`.

Redux store (`store.js`) manages language selection (Spanish/Portuguese/English). Language files in `langs/`.

**Testing:** 52 tests across 14 suites using Jest + `@testing-library/react`. Coverage: ~74% (scoped via `collectCoverageFrom` in `package.json`). Setup in `setupTests.js` mocks `react-translate-component` and `counterpart` with `__esModule = true` to handle CommonJS/ESM interop in Jest. Axios mock in `src/__mocks__/axios.js`.

### Deployment

- Backend: Docker on Heroku (`Backend/Dockerfile`, `Backend/heroku.yml`)
- Frontend: Firebase Hosting (`Frontend/firebase.json`)
- CI: Travis CI (`.travis.yml`) — builds and deploys both on master branch

## Key Model Relationships

`Substation` → has many `Transformator` → has many `Counter` → has `History` records

`Client` (linked to `CustomUser`) → `Contract` (links client to counter) → `Invoice` → `Payment`

`Worker` (linked to `CustomUser`) has a `user_type` field (1/2/3) determining role permissions.
