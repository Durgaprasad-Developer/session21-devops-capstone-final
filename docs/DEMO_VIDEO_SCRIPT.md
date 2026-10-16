# BookEase — Video Demonstration Script & Shot List (5–7 Minutes)

This document provides the exact scene-by-scene production script, terminal commands, visual cues, and voiceover guidelines for recording the **BookEase DevOps Capstone Demo Video**.

> [!TIP]
> 📺 **Recorded Video Demonstration**: [Watch on YouTube (5–7 mins)](https://www.youtube.com/watch?v=LMPvzXk0P0M)

> [!IMPORTANT]
> **Video Ground Rules**:
> - **Total Length**: 5 to 7 minutes.
> - **Authenticity**: Demonstrate the real, working local Kubernetes deployment, tests, and CI/CD pipeline.
> - **AWS Transparency**: Show and explain the Terraform IaC code and validation output; explain how BookEase deploys to EKS; **do not** claim a live AWS deployment.
> - **Resolution & Setup**: Record in 1080p (1920x1080) at 30/60 fps with high-contrast dark theme terminal (font size 16pt+).

---

## Shot List & Timeline Summary

| Scene # | Timestamp | Focus Topic | Active Screen | Speaking Goal |
|---|---|---|---|---|
| **Scene 1** | 0:00 – 0:45 | Introduction & Overview | Slide 1 + Repository root | Introduce BookEase domain and DevOps scope |
| **Scene 2** | 0:45 – 1:30 | Live Application Walkthrough | Browser: `http://localhost:3000` / Ingress | Demonstrate booking UI, doctors, and API docs |
| **Scene 3** | 1:30 – 2:15 | Automated Testing & Docker | Terminal: `pytest -v` & `docker compose ps` | Show 16 passing tests and non-root containers |
| **Scene 4** | 2:15 – 3:00 | CI/CD & DevSecOps Pipeline | GitHub Actions Run + GHCR Packages | Walk through test, build, Trivy scan, and SHA tags |
| **Scene 5** | 3:00 – 4:00 | Kubernetes, Helm & HPA | Terminal: `kubectl` & `helm list` | Demonstrate Deployments, Ingress, and HPA 2→5 |
| **Scene 6** | 4:00 – 4:45 | Prometheus & Grafana Monitoring | Browser: Prometheus Targets + Grafana | Show live metrics, latency p95, and request rates |
| **Scene 7** | 4:45 – 5:45 | AWS Terraform IaC & EKS v1.34 | VS Code / Terminal: `terraform` | Explain VPC, EKS v1.34 Standard Support, and cost |
| **Scene 8** | 5:45 – 6:15 | Conclusion & Rubric Wrap-up | Slide 14 + `docs/FINAL_AUDIT.md` | Summarize 90/100 verified score and final Q&A |

---

## Detailed Scene-by-Scene Script

### Scene 1: Introduction & Architecture Overview (0:00 – 0:45)
- **On-Screen**: Title Slide or GitHub Repository `README.md` at top.
- **Visual Action**: Scroll gently down to the Architecture Diagram.
- **Voiceover**:
  > *"Hello examiners and fellow engineers. My name is Durga Prasad, and this is BookEase, my DevOps Capstone project. BookEase is an enterprise-grade medical appointment management platform featuring patient records, doctor scheduling, and real-time dashboard analytics.*  
  > *In this demonstration, I will walk you through our complete end-to-end DevOps engineering stack: from hardened non-root containerization and automated Pytest testing to GitHub Actions CI/CD with Trivy DevSecOps gates, Kubernetes Helm orchestration with HPA autoscaling, Prometheus and Grafana observability, and our validated AWS Terraform infrastructure as code."*

---

### Scene 2: Live Application & REST API Walkthrough (0:45 – 1:30)
- **On-Screen**: Web Browser at BookEase Dashboard (`http://localhost:3000` or Ingress IP `http://192.168.49.2/`).
- **Visual Action**:
  1. Show the KPI summary cards (Total Appointments, Scheduled, Completed).
  2. Click on **Appointments**; show the appointment list table with status badges (`scheduled`, `completed`).
  3. Open a new tab to `/docs` (Swagger UI).
  4. Execute a quick curl in the terminal or Swagger:
     ```bash
     curl -s http://localhost:8000/health | jq .
     curl -s http://localhost:8000/ready | jq .
     ```
- **Voiceover**:
  > *"Here is the BookEase user interface. It is a React 18 single-page application served via an unprivileged Nginx reverse proxy. The dashboard displays live statistics aggregated from our PostgreSQL database.*  
  > *Navigating to the Appointments page, we can schedule, complete, or cancel appointments with conflict detection. Behind the frontend is our FastAPI backend, which exposes comprehensive REST endpoints documented here in Swagger at `/docs`.*  
  > *Notice our production health probes: `/health` provides a lightweight liveness probe, while `/ready` actively validates PostgreSQL database connectivity before serving customer traffic."*

---

### Scene 3: Automated Testing & Container Security (1:30 – 2:15)
- **On-Screen**: Split terminal window.
- **Visual Action**:
  1. In the backend directory, run:
     ```bash
     backend/.venv/bin/pytest -v
     ```
  2. Display the passing test output (`16 passed in 1.39s`).
  3. Inspect `backend/Dockerfile` and `frontend/Dockerfile` highlights:
     ```bash
     grep -E "USER|FROM" backend/Dockerfile frontend/Dockerfile
     ```
  4. Run `docker compose ps` to show healthy local services.
- **Voiceover**:
  > *"Reliable software starts with automated testing. Our test suite includes 16 automated Pytest tests validating appointment scheduling, doctor availability, overlapping conflict prevention, and error responses.*  
  > *These tests execute against an isolated in-memory SQLite database, guaranteeing that test runs never corrupt persistent data. All 16 tests pass in under 1.5 seconds.*  
  > *Turning to containerization, both our backend and frontend Dockerfiles strictly enforce non-root execution. The frontend utilizes a multi-stage build that compiles assets in Node 20 and serves them using an unprivileged Nginx Alpine runtime, significantly reducing the attack surface."*

---

### Scene 4: CI/CD Pipeline & DevSecOps Scanning (2:15 – 3:00)
- **On-Screen**: GitHub Actions Web UI (`.github/workflows/ci.yml` run).
- **Visual Action**:
  1. Show the green workflow graph with all 4 stages: `test`, `build-frontend`, `docker-build-scan`, `publish`.
  2. Click into the `docker-build-scan` job to highlight the Trivy Vulnerability Scan step.
  3. Switch to the GitHub Container Registry (GHCR) package page showing published images tagged with commit SHAs.
- **Voiceover**:
  > *"Every push to the main branch triggers our automated GitHub Actions CI/CD pipeline.*  
  > *The pipeline runs four sequential quality gates: first, it executes our Pytest suite; second, it compiles the production frontend bundle; third, it builds the container images and runs a Trivy vulnerability scan.*  
  > *Our DevSecOps policy strictly enforces zero HIGH and zero CRITICAL CVEs with `exit-code: 1`. Having remediated upstream library vulnerabilities, our images scan completely clean.*  
  > *Finally, verified images are published to GitHub Container Registry tagged with the exact Git commit SHA rather than a mutable latest tag, guaranteeing immutable and auditable deployments."*

---

### Scene 5: Kubernetes, Helm & Horizontal Pod Autoscaling (3:00 – 4:00)
- **On-Screen**: Terminal showing Kubernetes cluster state.
- **Visual Action**:
  1. Display deployed Helm chart:
     ```bash
     helm list -n bookease
     ```
  2. Inspect running workloads, pods, and ingress:
     ```bash
     kubectl get pods,svc,ingress,hpa -n bookease
     ```
  3. Highlight:
     - 2 Backend replicas (`appuser` non-root).
     - 2 Frontend replicas (`nginx` non-root).
     - 1 PostgreSQL pod with bound 2Gi PersistentVolumeClaim.
     - 1 Completed Alembic database migration Job.
     - Nginx Ingress routing traffic on Port 80.
  4. Reference the HPA test results in `docs/k8s_bookease_status.txt`:
     ```bash
     cat docs/k8s_bookease_status.txt | grep -A 10 "HORIZONTAL POD AUTOSCALER"
     ```
- **Voiceover**:
  > *"In Kubernetes, the application is packaged and deployed using our custom Helm chart located in `helm/bookease/`.*  
  > *Here in the `bookease` namespace, we run two backend replicas, two frontend replicas, a dedicated PostgreSQL stateful instance bound to a 2-gigabyte persistent volume, and an Alembic pre-migration job that auto-applies database schemas before traffic routes.*  
  > *All traffic enters through an Nginx Ingress controller that cleanly routes root traffic to the frontend and `/api` to the backend.*  
  > *We also configured Horizontal Pod Autoscaling (HPA v2) targeting 70% CPU. During our simulated load test with 35 concurrent workers, CPU reached 240%, causing the HPA to automatically scale our backend from 2 to 5 replicas to absorb the load, before gracefully stabilizing back to 2 replicas."*

---

### Scene 6: Observability with Prometheus & Grafana (4:00 – 4:45)
- **On-Screen**: Browser showing Prometheus UI and Grafana Dashboard.
- **Visual Action**:
  1. Show Prometheus Targets page (`/targets`) with `bookease-backend-pods` marked as **UP (1/1)**.
  2. Switch to Grafana Dashboard (`docs/screenshots/grafana_bookease_dashboard.png` or live UI at NodePort 32000).
  3. Point out the 6 live panels:
     - Active Backend Replicas (2)
     - Total Requests (>6,600)
     - Error Rate (0.00%)
     - p95 and p99 Request Latency
     - Throughput by Endpoint (req/s)
     - CPU & Memory RSS consumption
- **Voiceover**:
  > *"To ensure operability in production, we deployed Prometheus and Grafana in the `monitoring` namespace.*  
  > *Our FastAPI backend instrumentator exposes metrics at `/metrics`, which Prometheus scrapes every 10 seconds. As shown on the Targets page, the application is in an active `UP` state.*  
  > *In Grafana, our provisioned BookEase dashboard visualizes live application health across six panels: active pod replicas, cumulative requests served exceeding 6,600, error rates, p95 request latency, throughput by endpoint, and process memory utilization."*

---

### Scene 7: AWS Infrastructure as Code (Terraform) & Cost Model (4:45 – 5:45)
- **On-Screen**: VS Code editor viewing `terraform/` directory.
- **Visual Action**:
  1. Open `terraform/variables.tf` and highlight `cluster_version = "1.34"`.
  2. Open `terraform/networking.tf` and show VPC with 2 public subnets and 2 private subnets across 2 AZs.
  3. In terminal, run:
     ```bash
     cd terraform
     terraform fmt -check
     terraform init -backend=false
     terraform validate
     ```
  4. Show clean output: `Success! The configuration is valid.`
  5. Display the Cost Comparison Table from `README.md`.
- **Voiceover**:
  > *"Now let's examine our AWS cloud infrastructure defined in `terraform/`.*  
  > *Our IaC configures an enterprise Amazon VPC spanning two Availability Zones in Mumbai (`ap-south-1`), with two public subnets for load balancers and two private subnets for EKS worker nodes, egressed through a cost-optimized NAT Gateway.*  
  > *Critically, we updated our EKS cluster version to Kubernetes 1.34. In AWS EKS, older versions like 1.30 enter Extended Support, incurring an extra $0.50 per hour surcharge—amounting to $360 extra per month. Version 1.34 is covered under Standard Support through December 2026 at the standard $0.10 per hour rate.*  
  > *All Terraform files pass `terraform fmt`, `terraform init`, and `terraform validate` cleanly.*  
  > *In alignment with instructor guidance to prevent runaway student AWS bills, live cloud provisioning is kept at zero dollars, while our local Kubernetes cluster fully proves the live application."*

---

### Scene 8: Conclusion & Rubric Compliance (5:45 – 6:15)
- **On-Screen**: Display `docs/FINAL_AUDIT.md` summary table.
- **Visual Action**: Highlight the 90/100 verified score and the clean audit trail.
- **Voiceover**:
  > *"To conclude, BookEase satisfies all 10 modules of the DevOps capstone rubric with 90 out of 100 points fully verified with reproducible terminal logs and screenshots.*  
  > *The application runs reliably, the pipeline is fully automated and secure, the Kubernetes cluster auto-scales under load, and our Terraform IaC is verified and cost-optimized.*  
  > *Thank you for your time, and I look forward to your evaluation."*

---

## Recording Tips & Checklist

1. **Before Recording**:
   - Close all background notifications, chat apps, and browser tabs.
   - Set terminal prompt to clean format: `PS1='$ '` or standard bash.
   - Pre-open tabs:
     1. Local app: `http://localhost:3000`
     2. Swagger docs: `http://localhost:8000/docs`
     3. GitHub Actions CI page: `https://github.com/Durgaprasad-Developer/session21-devops-capstone-final/actions`
     4. GHCR packages page
     5. Prometheus & Grafana screenshots or UI tabs
2. **Audio Check**:
   - Speak clearly at a moderate pace (130–145 words per minute).
   - Use a USB headset or external microphone with noise suppression enabled.
3. **Export Settings & Delivery**:
   - Format: MP4 (H.264 video codec, AAC audio).
   - Published YouTube Video: [https://www.youtube.com/watch?v=LMPvzXk0P0M](https://www.youtube.com/watch?v=LMPvzXk0P0M)
   - Local/Offline Reference: `demo/bookease_demo_video.mp4` (or referenced in `README.md` and `docs/DEMO.md`).
