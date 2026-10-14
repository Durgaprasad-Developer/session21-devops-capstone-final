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

## Kubernetes & Helm Deployment (Minikube / Production)

The application is packaged with a production-style Helm chart in `helm/bookease`:

- **Multi-replica Deployments**: Backend (min 2, max 5) and Frontend (min 2, max 5) running as non-root users.
- **Persistence**: Dedicated PostgreSQL deployment backed by a 2Gi `PersistentVolumeClaim`.
- **Database Migrations**: Automated Alembic migration job executed via Helm pre-start init containers.
- **Ingress**: Unified Nginx Ingress routing `/` to the React SPA and `/api`, `/health`, `/ready`, `/metrics`, and `/docs` to the FastAPI backend.

```bash
# 1. Deploy BookEase using Helm
helm upgrade --install bookease ./helm/bookease \
  --namespace bookease \
  --create-namespace

# 2. Verify all pods and ingress
kubectl get pods,svc,ingress,hpa -n bookease

# 3. Access BookEase
MINIKUBE_IP=$(minikube ip)
curl http://$MINIKUBE_IP/health
curl http://$MINIKUBE_IP/api/doctors
```

---

## Horizontal Pod Autoscaling (HPA)

Autoscaling is configured with Kubernetes `autoscaling/v2`:

- **Metric**: CPU Utilization target `70%`.
- **Scaling Limits**: Min 2 pods, Max 5 pods per component.
- **Verification**: Evaluated with live concurrent traffic bursts; observed scale-up from 2 to 5 replicas within 70 seconds.

```bash
# View active HPA status and pod metrics
kubectl get hpa -n bookease
kubectl top pods -n bookease
```

---

## Observability & Monitoring (Prometheus + Grafana)

The monitoring stack is deployed in the `monitoring` namespace using maintained Helm charts:

- **Prometheus** (`prometheus-community/prometheus`): Scrapes BookEase FastAPI `/metrics` every 10 seconds.
- **Grafana** (`grafana/grafana`): Pre-provisioned with Prometheus datasource and the BookEase custom dashboard.
- **FastAPI Instrumentator**: Exposes HTTP request rates, status breakdown, latency histograms, and process metrics.

| Service | Minikube URL | Port-Forward | Credentials |
|---|---|---|---|
| **Prometheus UI** | `http://<MINIKUBE_IP>:32090` | `kubectl port-forward -n monitoring svc/prometheus-server 9090:9090` | None |
| **Grafana Dashboard** | `http://<MINIKUBE_IP>:32000` | `kubectl port-forward -n monitoring svc/grafana 3000:80` | `admin` / `adminpassword` |

### Key Grafana Metrics Panels

- **Active Backend Replicas**: Live count of healthy pods (`count(up{job="bookease-backend-pods"} == 1)`)
- **Total HTTP Requests**: Cumulative counter (`sum(http_requests_total)`)
- **HTTP Error Rate %**: Ratio of 4xx/5xx responses to total requests
- **Request Latency (p95 & p99)**: Quantiles computed from `http_request_duration_seconds_bucket`
- **CPU & Memory Usage**: Pod-level process CPU and RSS memory consumption

---

## Infrastructure as Code (Terraform AWS EKS)

The `terraform/` directory provisions production AWS infrastructure:
- Custom VPC with public and private subnets across 2 Availability Zones.
- Internet Gateway and NAT Gateway for private egress.
- AWS EKS Cluster (Kubernetes 1.30) with managed node groups.
- *Note*: AWS provisioning is safely deferred until cloud credentials and billing budgets are configured. All workloads are fully verified on local Minikube.

