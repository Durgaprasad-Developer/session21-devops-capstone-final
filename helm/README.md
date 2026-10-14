# BookEase — Helm Chart

This directory contains the production-style Helm chart for deploying BookEase on Kubernetes (Minikube or AWS EKS).

## Architecture

- **Frontend Deployment**: 2 Replicas, non-root user (uid 100), Nginx static server.
- **Backend Deployment**: 2 Replicas, non-root user (uid 100), FastAPI with health & readiness probes, Prometheus annotations.
- **Database Migration Job**: Dedicated Kubernetes Job running Alembic migrations once before backend replicas start.
- **PostgreSQL**: Deployment with PersistentVolumeClaim (2Gi storage) for reliable data persistence.
- **Services**: ClusterIP services for frontend, backend, and postgres.
- **Ingress**: Nginx Ingress routing `/` to the frontend and `/api`, `/health`, `/ready`, `/metrics`, and `/docs` to the backend.

## Quick Start (Minikube)

```bash
# 1. Start Minikube with Ingress
minikube start --driver=docker
minikube addons enable ingress

# 2. Deploy Helm Chart
helm install bookease ./helm/bookease --namespace bookease --create-namespace

# 3. Verify Pods and Ingress
kubectl get pods -n bookease
kubectl get ingress -n bookease

# 4. Access Application
MINIKUBE_IP=$(minikube ip)
curl http://$MINIKUBE_IP/health
curl http://$MINIKUBE_IP/api/appointments
```

## Chart Values Reference

| Parameter | Description | Default |
|---|---|---|
| `backend.replicaCount` | Number of backend replicas | `2` |
| `backend.image.repository` | Backend container image repository | `ghcr.io/durgaprasad-developer/session21-devops-capstone-final/bookease-backend` |
| `backend.image.tag` | Backend container image tag | `2be5d623eaea9c958783803ba3d8a8b89e7e0a79` |
| `frontend.replicaCount` | Number of frontend replicas | `2` |
| `frontend.image.repository` | Frontend container image repository | `ghcr.io/durgaprasad-developer/session21-devops-capstone-final/bookease-frontend` |
| `frontend.image.tag` | Frontend container image tag | `2be5d623eaea9c958783803ba3d8a8b89e7e0a79` |
| `postgresql.persistence.size` | PVC storage size for PostgreSQL | `2Gi` |
| `ingress.enabled` | Enable Kubernetes Ingress resource | `true` |
| `ingress.className` | Ingress controller class name | `nginx` |
