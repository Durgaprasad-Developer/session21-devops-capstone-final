# BookEase — Observability Stack (Prometheus + Grafana)

This directory contains the production Helm values, scrape configurations, and pre-built Grafana dashboards for BookEase observability.

## Architecture

- **Prometheus**: Deployed in `monitoring` namespace using the `prometheus-community/prometheus` Helm chart.
  - Scrapes the BookEase FastAPI `/metrics` endpoint every 10 seconds.
  - Supports both static service resolution (`bookease-backend.bookease.svc.cluster.local:8000`) and dynamic Kubernetes pod discovery.
  - Exposes Prometheus UI on NodePort `32090`.
- **Grafana**: Deployed in `monitoring` namespace using the `grafana/grafana` Helm chart.
  - Pre-configured with Prometheus as default data source (`http://prometheus-server.monitoring.svc.cluster.local:9090`).
  - Pre-loaded with custom dashboard: `BookEase — Application Metrics & Observability` (`bookease-observability`).
  - Exposes Grafana dashboard on NodePort `32000`.
- **Kube State Metrics**: Provides cluster-level metrics (pod readiness, deployment replicas, container restarts).

---

## Accessing the Monitoring Tools

| Service | Minikube URL | Port-Forward Option | Credentials |
|---|---|---|---|
| **Prometheus UI** | `http://<MINIKUBE_IP>:32090` | `kubectl port-forward -n monitoring svc/prometheus-server 9090:9090` | None |
| **Grafana UI** | `http://<MINIKUBE_IP>:32000` | `kubectl port-forward -n monitoring svc/grafana 3000:80` | `admin` / `adminpassword` |

---

## Grafana Dashboard Panels

The dashboard (`monitoring/dashboards/bookease-dashboard.json`) tracks:

1. **Active Backend Replicas**: `count(up{job="bookease-backend-pods"} == 1)`
2. **Total HTTP Requests**: `sum(http_requests_total)`
3. **HTTP Error Rate %**: `(sum(rate(http_requests_total{status=~"[45].*"}[1m])) or 0) / sum(rate(http_requests_total[1m])) * 100`
4. **Request Latency (p95)**: `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[1m])) by (le))`
5. **Request Rate by Endpoint**: `sum(rate(http_requests_total[1m])) by (handler)`
6. **Backend Process CPU Usage**: `sum(rate(process_cpu_seconds_total[1m])) by (instance) * 100`
7. **Backend Memory Usage (RSS)**: `sum(process_resident_memory_bytes) by (instance)`

---

## Deployment Commands

```bash
# 1. Add Helm repositories
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# 2. Create ConfigMap for Grafana Dashboard
kubectl create configmap bookease-grafana-dashboards \
  --from-file=bookease-dashboard.json=monitoring/dashboards/bookease-dashboard.json \
  -n monitoring --dry-run=client -o yaml | kubectl apply -f -

# 3. Deploy Prometheus
helm upgrade --install prometheus prometheus-community/prometheus \
  -f monitoring/prometheus-values.yaml \
  -n monitoring --create-namespace

# 4. Deploy Grafana
helm upgrade --install grafana grafana/grafana \
  -f monitoring/grafana-values.yaml \
  -n monitoring

# 5. Verify Target Status
curl -s http://$(minikube ip):32090/api/v1/targets | jq '.data.activeTargets[] | {job: .labels.job, health: .health}'
```

---

## Evidence Screenshots

- **Prometheus Targets UP**: `docs/screenshots/prometheus_targets_up.png`
- **Grafana Populated Dashboard**: `docs/screenshots/grafana_bookease_dashboard.png`
- **FastAPI `/metrics` Output**: `docs/metrics_output.txt`
