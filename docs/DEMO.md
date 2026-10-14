# BookEase — DevOps Capstone Demo Walkthrough (5–7 Minutes)

This presentation guide provides a structured, step-by-step walkthrough of the BookEase Appointment Management System and its complete DevOps engineering stack for examiners and peer evaluators.

---

## 1. Project Overview & Architecture (1 Minute)

- **Domain**: BookEase is an enterprise-grade medical appointment management platform with appointment scheduling, doctor availability management, patient records, and real-time dashboard KPIs.
- **Full Architecture**:
  - **Frontend**: React 18, Vite 5, Nginx 1.27 unprivileged reverse proxy.
  - **Backend**: Python 3.12, FastAPI, SQLAlchemy 2.x, Alembic migrations, Prometheus FastApi Instrumentator.
  - **Database**: PostgreSQL 16 with persistent volumes.
  - **DevOps Layer**:
    - Multi-stage non-root containerization.
    - Automated CI/CD pipeline on GitHub Actions with Trivy DevSecOps gates.
    - GHCR container registry publishing with Git commit SHA tags.
    - Production Terraform IaC for AWS VPC, public/private subnets, and EKS.
    - Production Helm chart with Ingress, Secrets, ConfigMaps, and PersistentVolumeClaims.
    - Kubernetes Horizontal Pod Autoscaler (HPA v2) responding to CPU pressure.
    - Prometheus & Grafana observability stack with pre-built dashboards.

---

## 2. Live Application & REST API (1 Minute)

### Local Access Points
- **Frontend SPA**: `http://192.168.49.2/` (via Minikube Ingress) or `http://localhost:3000` (Docker Compose)
- **Backend API & Swagger Docs**: `http://192.168.49.2/docs`
- **Health Check**: `http://192.168.49.2/health`
- **Readiness Check**: `http://192.168.49.2/ready`
- **Prometheus Metrics**: `http://192.168.49.2/metrics`

### Demonstration Commands
```bash
# Verify Health & Readiness
curl -s http://192.168.49.2/health | jq .
curl -s http://192.168.49.2/ready | jq .

# Query Doctors
curl -s http://192.168.49.2/api/doctors | jq '.[0]'

# Create an Appointment via API
curl -s -X POST http://192.168.49.2/api/appointments \
  -H "Content-Type: application/json" \
  -d '{"patient_name":"Rahul Sharma","patient_email":"rahul@example.com","doctor_id":1,"appointment_date":"2026-10-25","start_time":"10:00:00","end_time":"10:30:00","reason":"Routine checkup"}' | jq .
```

---

## 3. Automated Testing & Code Quality (30 Seconds)

16 automated unit tests run against an isolated SQLite test database, validating all business logic, overlapping appointment conflict prevention, and CRUD operations.

```bash
cd backend
source .venv/bin/activate
pytest -v
```
*Expected Result*: `16 passed in ~1.5s`

---

## 4. GitHub Actions CI/CD & DevSecOps (1 Minute)

- **Workflow File**: [`.github/workflows/ci.yml`](file:///home/durga-prasad/session21-devops-capstone-final/.github/workflows/ci.yml)
- **Quality Gates**:
  1. `test`: Sets up Python 3.12, runs Alembic migrations on SQLite, and executes Pytest. Fails build on test error.
  2. `build-frontend`: Builds production Vite bundle to catch static asset errors.
  3. `docker-build-scan`:
     - Builds Docker images for backend and frontend.
     - Runs **Trivy vulnerability scan** on both images.
     - Enforces `exit-code: '1'` and `severity: 'CRITICAL,HIGH'`.
     - Scans pass with **zero HIGH or CRITICAL findings**.
  4. `publish`: Publishes images to GitHub Container Registry (GHCR) tagged with the exact Git commit SHA:
     - `ghcr.io/durgaprasad-developer/session21-devops-capstone-final/bookease-backend:2be5d623eaea9c958783803ba3d8a8b89e7e0a79`
     - `ghcr.io/durgaprasad-developer/session21-devops-capstone-final/bookease-frontend:2be5d623eaea9c958783803ba3d8a8b89e7e0a79`

---

## 5. Kubernetes & Helm Deployment (1 Minute)

The application is deployed to the `bookease` namespace using our custom Helm chart:

```bash
# View all deployed components
kubectl get pods,svc,hpa,ingress -n bookease
```

### Key Elements to Highlight
1. **Multi-Replica Pods**: Backend and Frontend running 2 replicas each (scaled up to 5 by HPA).
2. **PostgreSQL Persistence**: 2Gi PersistentVolumeClaim bound to `bookease-postgres`.
3. **Automated Migrations**: One-off Kubernetes batch job runs `alembic upgrade head` before backend pods receive traffic.
4. **Ingress**: Single Nginx Ingress routes `/` to Frontend and `/api`, `/health`, `/ready`, `/metrics`, `/docs` to Backend.

---

## 6. Horizontal Pod Autoscaling (HPA) in Action (1 Minute)

- **Target**: CPU utilization target `70%`.
- **Scaling Range**: Min 2 pods, Max 5 pods per component.

### Observed Live Scaling Behavior
During the load test (35 concurrent workers hammering `/api/doctors`), the following transition was recorded:
1. **Initial**: 2 Replicas, CPU at 2%.
2. **Under Load**: CPU surged to 240% (238m per pod against a 100m request).
3. **Scale Up**: HPA controller automatically scaled backend deployment to **4 replicas**, then to **5 replicas** (`maxReplicas`).
4. **Stabilization**: Once traffic ceased, replicas scaled back to 2 following the stabilization window.

```bash
# Inspect current HPA state
kubectl get hpa -n bookease
```

---

## 7. Observability: Prometheus & Grafana (1 Minute)

- **Namespace**: `monitoring`
- **Prometheus UI**: `http://192.168.49.2:32090`
- **Grafana Dashboard**: `http://192.168.49.2:32000` (User: `admin` / Password: `adminpassword`)

```bash
# Verify Prometheus target status
curl -s http://192.168.49.2:32090/api/v1/targets | jq '.data.activeTargets[] | {job: .labels.job, health: .health}'
```

### Dashboard Panels Demonstrated
- **Backend Active Replicas**: Live count of healthy pods.
- **Total HTTP Requests**: Cumulative counter (>6,600 requests served).
- **HTTP Error Rate %**: Real-time error percentage.
- **Request Latency (p95 & p99)**: Latency quantiles from histogram buckets.
- **HTTP Request Rate by Endpoint**: Per-route throughput (`/api/doctors`, `/api/appointments`, `/health`).
- **Backend CPU & Memory Usage**: Pod-level process CPU utilization and resident memory.

---

## 8. Terraform AWS Infrastructure Status (30 Seconds)

- **Location**: `terraform/`
- **Configuration**: Fully written, formatted (`terraform fmt -check`), and validated (`terraform validate`).
- **Resources Defined (33 resources)**:
  - Custom VPC (`10.0.0.0/16`) in `ap-south-1`.
  - 2 Public Subnets + 2 Private Subnets across 2 Availability Zones.
  - Internet Gateway + NAT Gateway for secure private egress.
  - AWS EKS Cluster (v1.34 Standard Support) + Managed Node Group (`t3.medium`, autoscaling 1–4 nodes).
- **Deployment Rationale**:
  - Offline validation (`terraform fmt -check`, `terraform init -backend=false`, `terraform validate`) passes cleanly.
  - **AWS live provisioning is deliberately deferred** until AWS account credentials and budget are allocated, preventing unintentional cloud charges (~$5.60/day).
  - The entire application and Kubernetes stack is completely verified on local Minikube.

---

## 9. Cleanup Commands

```bash
# Stop Minikube cluster
minikube stop

# Or uninstall Helm releases while preserving local disk
helm uninstall bookease -n bookease
helm uninstall grafana -n monitoring
helm uninstall prometheus -n monitoring
```
