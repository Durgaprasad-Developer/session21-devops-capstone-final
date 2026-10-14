# BookEase — Appointment Booking Management System

BookEase is a full-stack appointment management application built as the DevOps Capstone Final Project (Session 21).

## Technology Stack

| Layer       | Technology                          |
|-------------|-------------------------------------|
| Frontend    | React 18 + Vite 5 + Nginx           |
| Backend     | FastAPI + Python 3.12               |
| ORM         | SQLAlchemy 2.x                      |
| Database    | PostgreSQL 16                       |
| Migrations  | Alembic                             |
| Tests       | Pytest + SQLite (isolated)          |
| Containers  | Docker + Docker Compose             |
| Metrics     | Prometheus (prometheus-fastapi-instrumentator) |

## Features

- **Dashboard** — KPI cards with live stats (total, today, upcoming, completed, cancelled)
- **Appointments** — Full CRUD with search, status filter, date/time picker, doctor overlap detection
- **Doctors** — Manage doctors, specialities, and availability windows
- **Patients** — Manage patient records and contact details

## Quick Start (Docker Compose)

```bash
git clone <your-repo-url>
cd session21-devops-capstone-final

docker compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Metrics: http://localhost:8000/metrics

## Run Backend Locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export DATABASE_URL='postgresql+psycopg://bookease:bookease@localhost:5432/bookease'
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

## Tests

```bash
cd backend
pip install -r requirements.txt
pytest -v
```

Tests use an isolated SQLite database — no PostgreSQL required.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | / | Root |
| GET | /health | Liveness |
| GET | /ready | Readiness (DB check) |
| GET | /metrics | Prometheus metrics |
| GET | /api/appointments | List appointments |
| POST | /api/appointments | Create appointment |
| GET | /api/appointments/{id} | Get appointment |
| PUT | /api/appointments/{id} | Update appointment |
| DELETE | /api/appointments/{id} | Delete appointment |
| GET | /api/appointments/stats | Dashboard stats |
| GET | /api/doctors | List doctors |
| POST | /api/doctors | Create doctor |
| GET | /api/doctors/{id} | Get doctor |
| PUT | /api/doctors/{id} | Update doctor |
| DELETE | /api/doctors/{id} | Delete doctor |
| GET | /api/patients | List patients |
| POST | /api/patients | Create patient |
| GET | /api/patients/{id} | Get patient |
| PUT | /api/patients/{id} | Update patient |
| DELETE | /api/patients/{id} | Delete patient |

## Repository Structure

```
session21-devops-capstone-final/
├── backend/
│   ├── app/
│   │   ├── main.py         # FastAPI app entry
│   │   ├── models.py       # SQLAlchemy models
│   │   ├── schemas.py      # Pydantic schemas
│   │   ├── crud.py         # Business logic
│   │   ├── database.py     # DB config
│   │   └── routers/        # API routers
│   ├── alembic/            # DB migrations
│   ├── tests/              # Pytest tests
│   ├── Dockerfile
│   ├── requirements.txt
│   └── pytest.ini
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Root + sidebar nav
│   │   ├── api.js          # API client
│   │   ├── index.css       # Global styles
│   │   └── pages/          # Dashboard, Appointments, Doctors, Patients
│   ├── nginx.conf
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
├── .env.example
└── README.md
```

## DevOps Pipeline (Phase 2+)

- GitHub Actions CI/CD
- Trivy security scanning
- GHCR image publishing
- Terraform (AWS VPC + EKS)
- Kubernetes + Helm
- HPA
- Prometheus + Grafana
