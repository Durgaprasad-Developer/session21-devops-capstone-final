#!/usr/bin/env python3
"""
Generate a professional, high-impact 16:9 PowerPoint presentation for BookEase DevOps Capstone.
Includes complete coverage of modules M1 to M10, AWS Terraform design, cost models, and evidence.
"""

import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_paths):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Color Palette
    BG_DARK = RGBColor(15, 23, 42)      # Slate 900
    CARD_BG = RGBColor(30, 41, 59)      # Slate 800
    CARD_BORDER = RGBColor(51, 65, 85)  # Slate 700
    ACCENT_CYAN = RGBColor(14, 165, 233)# Sky 500
    ACCENT_TEAL = RGBColor(20, 184, 166)# Teal 500
    TEXT_WHITE = RGBColor(248, 250, 252)# Slate 50
    TEXT_MUTED = RGBColor(148, 163, 184)# Slate 400
    ACCENT_GREEN = RGBColor(34, 197, 94)# Green 500

    def add_header(slide, title_text, category_text="BOOKEASE DEVOPS CAPSTONE"):
        # Category tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_CYAN

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(26)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

    def add_card(slide, left, top, width, height, title, items, badge=""):
        # Card background shape
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = CARD_BG
        shape.line.color.rgb = CARD_BORDER
        shape.line.width = Pt(1)

        # Content textbox
        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(16)
        p_t.font.bold = True
        p_t.font.color.rgb = ACCENT_TEAL
        p_t.space_after = Pt(10)

        for item in items:
            p_i = tf.add_paragraph()
            p_i.text = f"•  {item}"
            p_i.font.size = Pt(12)
            p_i.font.color.rgb = TEXT_WHITE
            p_i.space_after = Pt(6)

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 1: Title Slide
    # ─────────────────────────────────────────────────────────────────────────
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = BG_DARK
    bg1.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(4.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p_badge = tf1.paragraphs[0]
    p_badge.text = "SESSION 21 — DEVOPS FINAL CAPSTONE PROJECT"
    p_badge.font.size = Pt(13)
    p_badge.font.bold = True
    p_badge.font.color.rgb = ACCENT_CYAN
    p_badge.space_after = Pt(14)

    p_main = tf1.add_paragraph()
    p_main.text = "BookEase: Scalable Appointment Booking Platform"
    p_main.font.size = Pt(36)
    p_main.font.bold = True
    p_main.font.color.rgb = TEXT_WHITE
    p_main.space_after = Pt(12)

    p_sub = tf1.add_paragraph()
    p_sub.text = "End-to-End Cloud DevOps: From Containerization & CI/CD to Kubernetes, HPA, Prometheus & AWS Terraform IaC"
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = TEXT_MUTED
    p_sub.space_after = Pt(28)

    p_meta = tf1.add_paragraph()
    p_meta.text = "Candidate: Durga Prasad  |  Repository: session21-devops-capstone-final  |  Evaluated Score: 90/100 (Full Local & IaC Proof)"
    p_meta.font.size = Pt(13)
    p_meta.font.bold = True
    p_meta.font.color.rgb = ACCENT_TEAL

    s1.notes_slide.notes_text_frame.text = (
        "Welcome examiners. Today I present BookEase, a complete SaaS medical appointment management system. "
        "More than just an app, this project demonstrates how code travels from local development through automated "
        "quality gates, container security, and Kubernetes orchestration to production-ready AWS Terraform infrastructure."
    )

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 2: Executive Summary & Project Goals
    # ─────────────────────────────────────────────────────────────────────────
    s2 = prs.slides.add_slide(blank_layout)
    bg2 = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg2.fill.solid()
    bg2.fill.fore_color.rgb = BG_DARK
    bg2.line.fill.background()
    add_header(s2, "Executive Summary: Business Domain & DevOps Pillars")

    add_card(s2, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.0),
             "1. Business Application", [
                 "Enterprise medical appointment platform with patient records and doctor scheduling.",
                 "FastAPI Python 3.12 backend with SQLAlchemy 2 and Alembic schema migrations.",
                 "Modern React 18 + Vite frontend served via unprivileged Nginx reverse proxy.",
                 "Comprehensive REST API covering full CRUD, statistics, and health probes."
             ])

    add_card(s2, Inches(4.8), Inches(1.8), Inches(3.7), Inches(5.0),
             "2. Quality & Security Gates", [
                 "16 automated Pytest unit tests running against isolated in-memory test database.",
                 "GitHub Actions CI/CD triggered on push to main with zero manual steps.",
                 "Trivy container security scanning enforcing 0 HIGH and 0 CRITICAL CVEs.",
                 "Immutable container image publishing to GHCR with exact Git commit SHA tags."
             ])

    add_card(s2, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0),
             "3. Cloud Infrastructure", [
                 "Production Helm chart with Ingress, multi-replica Deployments, and PVCs.",
                 "Horizontal Pod Autoscaling (HPA v2) proven under live stress testing (2→5 pods).",
                 "Prometheus & Grafana observability stack with 6 populated live panels.",
                 "Modular AWS Terraform IaC aligned to EKS Standard Support v1.34 ($0 cost mode)."
             ])

    s2.notes_slide.notes_text_frame.text = (
        "BookEase solves a real-world booking concurrency problem while strictly satisfying every requirement "
        "of the 10 DevOps Capstone modules. We prioritized production-grade engineering: non-root containers, "
        "security scanning gates, automated migrations, and zero-leak cloud infrastructure as code."
    )

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 3: End-to-End System Architecture
    # ─────────────────────────────────────────────────────────────────────────
    s3 = prs.slides.add_slide(blank_layout)
    bg3 = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg3.fill.solid()
    bg3.fill.fore_color.rgb = BG_DARK
    bg3.line.fill.background()
    add_header(s3, "System Architecture: Local Cluster vs. AWS Cloud Design")

    add_card(s3, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Local Verified Cluster (Minikube / Helm)", [
                 "Ingress Controller: Nginx Ingress at 192.168.49.2 routing '/' and '/api'.",
                 "Frontend Workload: 2x React 18 SPA pods (Nginx unprivileged, Port 80).",
                 "Backend Workload: 2-5x FastAPI pods (Port 8000) auto-scaled by HPA on CPU.",
                 "Database: PostgreSQL 16 stateful pod with bound 2Gi PersistentVolumeClaim.",
                 "Init Job: Kubernetes Batch Job executing 'alembic upgrade head' at boot.",
                 "Observability: Prometheus server (NodePort: 32090) scraping backend /metrics; Grafana UI (NodePort: 32000) showing live latency and request rates."
             ])

    add_card(s3, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "Target AWS Production Architecture (Terraform IaC)", [
                 "Amazon VPC: 10.0.0.0/16 across 2 Availability Zones (ap-south-1a & 1b).",
                 "Subnet Isolation: 2 Public subnets for ALBs/IGW; 2 Private subnets for EKS worker nodes.",
                 "Egress: Single cost-optimized NAT Gateway with Elastic IP for private worker outbound.",
                 "EKS Control Plane: Managed Kubernetes v1.34 with private & public API endpoints.",
                 "Managed Node Group: 2x t3.medium EC2 instances (scaling 1-4) with 20GiB gp3 disks.",
                 "EKS Add-ons: vpc-cni, CoreDNS, and kube-proxy managed declaratively in Terraform.",
                 "Cost Control: Kept in validated IaC state ($0.00 spent) to prevent student bill overrun."
             ])

    s3.notes_slide.notes_text_frame.text = (
        "Here we show the clear architecture separation: our local deployment is 100% live and verified, "
        "proving the application, database persistence, Ingress routing, HPA autoscaling, and Prometheus metrics. "
        "In parallel, our Terraform code defines the exact AWS VPC, subnets, NAT, and EKS v1.34 infrastructure."
    )

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 4: M1 — Application Architecture & REST API
    # ─────────────────────────────────────────────────────────────────────────
    s4 = prs.slides.add_slide(blank_layout)
    bg4 = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg4.fill.solid()
    bg4.fill.fore_color.rgb = BG_DARK
    bg4.line.fill.background()
    add_header(s4, "Module M1: Application, Data Model & REST Endpoints")

    add_card(s4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "FastAPI Backend & Data Model", [
                 "FastAPI 0.115+ framework with Pydantic v2 data validation schemas.",
                 "Three relational entities: Patients, Doctors (with specialty and availability hours), and Appointments.",
                 "Business Logic: Automatic conflict rejection if overlapping appointments are scheduled with the same doctor.",
                 "Automated Database Migrations: Alembic tracks schema changes; 001_initial_schema creates tables cleanly.",
                 "Interactive Documentation: Swagger UI live at /docs and OpenAPI at /openapi.json."
             ])

    add_card(s4, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "Production Health Probes & Endpoints", [
                 "GET /health: Lightweight liveness probe returning {'status':'healthy'}.",
                 "GET /ready: Readiness probe executing 'SELECT 1' against PostgreSQL to verify active DB connection before serving traffic.",
                 "GET /metrics: Prometheus machine-readable metrics (FastAPI Instrumentator).",
                 "REST APIs: Full CRUD across /api/appointments, /api/doctors, and /api/patients.",
                 "GET /api/appointments/stats: Live KPI aggregation (total, scheduled, completed, cancelled) for dashboard cards."
             ])

    s4.notes_slide.notes_text_frame.text = (
        "For M1, BookEase exceeds the baseline requirements. We implemented 12 REST endpoints across doctors, "
        "patients, and appointments, alongside dedicated liveness (/health) and database readiness (/ready) checks."
    )

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 5: M2 & M3 — Automated Testing & Git Quality
    # ─────────────────────────────────────────────────────────────────────────
    s5 = prs.slides.add_slide(blank_layout)
    bg5 = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg5.fill.solid()
    bg5.fill.fore_color.rgb = BG_DARK
    bg5.line.fill.background()
    add_header(s5, "Modules M2 & M3: Testing Suite & Repository Hygiene")

    add_card(s5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "M2: 16 Passing Pytest Unit Tests", [
                 "Test Isolation: Tests execute against an isolated in-memory SQLite database via conftest.py fixtures — production DB is never touched.",
                 "Appointment Scheduling: Tests create, update status, fetch by ID, and list appointments.",
                 "Doctor & Patient Management: Profile creation, availability validation, and deletion tests.",
                 "Validation & Error Handling: Verifies rejection when end_time is before start_time and when non-existent IDs are queried.",
                 "Health Endpoint Tests: Validates /health and /root response schemas.",
                 "Result: 16 passed, 0 failed in 1.39s (recorded in docs/pytest_output.txt)."
             ])

    add_card(s5, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "M3: Git Version Control & Hygiene", [
                 "Public GitHub Repository: https://github.com/Durgaprasad-Developer/session21-devops-capstone-final",
                 "12+ Semantic Commits: Using Conventional Commits (feat, fix, docs, chore).",
                 "Exclusion Rules (.gitignore): Strictly excludes .env, credentials, *.tfstate, .terraform/, __pycache__, and node_modules.",
                 "Zero Secret Leaks: Comprehensive repository scan confirms zero AWS access keys or passwords committed to Git history."
             ])

    s5.notes_slide.notes_text_frame.text = (
        "M2 testing features 16 automated test cases, far exceeding the 5-test rubric minimum. "
        "M3 ensures clean version control, semantic commit history, and strict secret protection."
    )

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 6: M4 — Containerization & Docker Compose
    # ─────────────────────────────────────────────────────────────────────────
    s6 = prs.slides.add_slide(blank_layout)
    bg6 = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg6.fill.solid()
    bg6.fill.fore_color.rgb = BG_DARK
    bg6.line.fill.background()
    add_header(s6, "Module M4: Hardened Containers & Docker Compose")

    add_card(s6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Hardened Multi-Stage Dockerfiles", [
                 "Backend (backend/Dockerfile): Python 3.12 slim base; runs as dedicated non-root user 'appuser' (UID:GID 100:101); includes curl for healthcheck.",
                 "Frontend (frontend/Dockerfile): Multi-stage build — Stage 1 compiles React assets using Node 20 Alpine; Stage 2 serves optimized static files via nginxinc/nginx-unprivileged:1.27-alpine (UID 101).",
                 "Security Posture: Dropped root privileges across all application containers to prevent privilege escalation vulnerabilities.",
                 "Optimized Image Size: Frontend image ~30MB; Backend image ~180MB."
             ])

    add_card(s6, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "Docker Compose Local Orchestration", [
                 "Three-Service Stack: frontend (Port 3000), backend (Port 8000), and postgres:16-alpine (Port 5432).",
                 "Dependency Management: Backend service waits for Postgres health check before starting.",
                 "Alembic Auto-Boot: Backend entrypoint applies pending database migrations on startup.",
                 "One-Command Startup: 'docker compose up --build -d' brings up the complete environment in under 30 seconds.",
                 "Verified Status: Recorded in docs/docker_compose_status.txt."
             ])

    s6.notes_slide.notes_text_frame.text = (
        "In M4, both Dockerfiles enforce non-root execution. The frontend utilizes multi-stage builds "
        "with an unprivileged Nginx base image, and Docker Compose provides one-click local stack execution."
    )

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 7: M5 & M6 — CI/CD Pipeline & DevSecOps
    # ─────────────────────────────────────────────────────────────────────────
    s7 = prs.slides.add_slide(blank_layout)
    bg7 = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg7.fill.solid()
    bg7.fill.fore_color.rgb = BG_DARK
    bg7.line.fill.background()
    add_header(s7, "Modules M5 & M6: GitHub Actions CI/CD & DevSecOps Gates")

    add_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "M5: Four-Stage Automated CI/CD", [
                 "Trigger: Automatically runs on every push to main in .github/workflows/ci.yml.",
                 "Stage 1 (test): Executes Pytest suite on Python 3.12 with SQLite. Pipeline halts immediately on failure.",
                 "Stage 2 (build-frontend): Runs 'npm run build' with Vite to catch static bundle defects.",
                 "Stage 3 (docker-build-scan): Builds Docker images for backend & frontend.",
                 "Stage 4 (publish): Pushes verified images to GitHub Container Registry (GHCR) tagged with the exact Git commit SHA (e.g., :2be5d62...)."
             ])

    add_card(s7, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "M6: Trivy Container Vulnerability Scan", [
                 "Strict DevSecOps Policy: Integrated aquasecurity/trivy-action in CI.",
                 "Failure Gate: Configured with 'exit-code: 1' and 'severity: CRITICAL,HIGH'.",
                 "Remediated Findings: Upgraded dependencies to resolve CVE-2025-62727 and patched OS libraries using Alpine security updates.",
                 "Clean Scan Result: Zero HIGH and zero CRITICAL CVEs present in published GHCR images.",
                 "GHCR Artifacts: Publicly accessible at ghcr.io/durgaprasad-developer/session21-devops-capstone-final."
             ])

    s7.notes_slide.notes_text_frame.text = (
        "M5 and M6 establish our automated quality gates. Every commit triggers automated unit testing, "
        "frontend compilation, and Trivy security scanning. Only images with zero High and Critical CVEs "
        "are tagged with the commit SHA and published to GHCR."
    )

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 8: M7 — AWS Infrastructure as Code (Terraform)
    # ─────────────────────────────────────────────────────────────────────────
    s8 = prs.slides.add_slide(blank_layout)
    bg8 = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg8.fill.solid()
    bg8.fill.fore_color.rgb = BG_DARK
    bg8.line.fill.background()
    add_header(s8, "Module M7: AWS Infrastructure as Code (Terraform)")

    add_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Terraform Modular IaC Architecture", [
                 "Provider & Tooling: HashiCorp AWS Provider ~> 5.50; Terraform >= 1.5.0, < 2.0.0.",
                 "VPC & Subnets: 10.0.0.0/16 VPC spanning 2 AZs (ap-south-1a, ap-south-1b). 2 Public subnets (10.0.1.0/24, 10.0.2.0/24) and 2 Private subnets (10.0.10.0/24, 10.0.20.0/24).",
                 "Subnet Tagging: Configured with kubernetes.io/role/elb=1 and kubernetes.io/role/internal-elb=1 for AWS Load Balancer discovery.",
                 "NAT Gateway: Cost-optimized single NAT Gateway with Elastic IP for worker node outbound connectivity.",
                 "Security Groups: EKS control plane and worker node ingress/egress rules."
             ])

    add_card(s8, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "EKS Control Plane & Worker Nodes", [
                 "Kubernetes Version: v1.34 under AWS Standard Support (avoids Extended Support charges).",
                 "IAM Least Privilege: Separate IAM roles for control plane (AmazonEKSClusterPolicy) and nodes (WorkerNodePolicy, CNI_Policy, ContainerRegistryReadOnly).",
                 "Managed Node Group: 2x t3.medium On-Demand nodes (scaling 1-4) with 20GiB gp3 disks.",
                 "Managed Add-ons: vpc-cni, coredns, and kube-proxy declared as first-class resources.",
                 "Safe Configurations: terraform.tfvars.example provided with zero committed credentials."
             ])

    s8.notes_slide.notes_text_frame.text = (
        "In M7, our Terraform code defines complete, enterprise-ready AWS infrastructure. "
        "It provisions a multi-AZ VPC, private/public subnets, NAT Gateway, IAM roles, and an EKS cluster with managed node groups."
    )

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 9: M7 Deep Dive — EKS Compatibility & Cost Analysis
    # ─────────────────────────────────────────────────────────────────────────
    s9 = prs.slides.add_slide(blank_layout)
    bg9 = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg9.fill.solid()
    bg9.fill.fore_color.rgb = BG_DARK
    bg9.line.fill.background()
    add_header(s9, "Module M7 Deep Dive: EKS Compatibility & Cost Comparison")

    add_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "EKS Version Alignment (1.30 vs 1.34)", [
                 "AWS Lifecycle Policy: EKS versions receive 14 months of Standard Support, after which they enter Extended Support.",
                 "Extended Support Penalty: EKS v1.30 incurs an additional $0.50/hour surcharge ($0.60/hr total), costing an extra ~$360/month!",
                 "Our Fix: Upgraded cluster_version to '1.34' in variables.tf and terraform.tfvars.example.",
                 "Lifecycle Benefit: Version 1.34 is covered under AWS Standard Support through December 2026 at the baseline $0.10/hour rate."
             ])

    add_card(s9, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "Deployment Modes & Cost Breakdown", [
                 "Mode A: Local Minikube / Compose = $0.00 / month (100% verified, active evidence).",
                 "Mode B: AWS EKS Standard (v1.34) = ~$5.60 / day (~$168 / month): EKS Control Plane ($73) + 2x t3.medium ($60) + NAT Gateway ($32) + EBS ($3).",
                 "Mode C: AWS EKS Extended (v1.30) = ~$17.60 / day (~$528 / month).",
                 "IaC Validation Proof: 'terraform fmt -check', 'terraform init -backend=false', and 'terraform validate' all pass with 0 errors.",
                 "Teardown Safety: Clear 'helm uninstall' followed by 'terraform destroy' sequence prevents orphaned load balancers."
             ])

    s9.notes_slide.notes_text_frame.text = (
        "This slide highlights our cost engineering. By aligning to EKS v1.34 Standard Support, "
        "we prevent an extra $360/month in AWS surcharges. Our Terraform configuration is fully validated, "
        "while live cloud creation is safely deferred to protect student budgets."
    )

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 10: M8 — Kubernetes & Helm Deployment
    # ─────────────────────────────────────────────────────────────────────────
    s10 = prs.slides.add_slide(blank_layout)
    bg10 = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg10.fill.solid()
    bg10.fill.fore_color.rgb = BG_DARK
    bg10.line.fill.background()
    add_header(s10, "Module M8: Kubernetes Orchestration & Helm Chart")

    add_card(s10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Production Helm Chart (helm/bookease)", [
                 "Chart Structure: Chart.yaml (v1.0.0), values.yaml, and 12 Kubernetes templates.",
                 "Backend Deployment: 2 replicas, CPU/memory requests and limits, liveness & readiness HTTP probes.",
                 "Frontend Deployment: 2 replicas, unprivileged Nginx runtime, Port 80 ClusterIP.",
                 "PostgreSQL Stateful Workload: Bound to 2Gi PersistentVolumeClaim (bookease-postgres-data).",
                 "Pre-flight Database Migration: Kubernetes batch Job executes Alembic migrations prior to traffic serving.",
                 "Clean Deployment: 'helm upgrade --install bookease ./helm/bookease' deployed with 0 errors."
             ])

    add_card(s10, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "Traffic Routing & HPA Autoscaling", [
                 "Nginx Ingress Routing: Single Ingress routes '/' to frontend and '/api', '/health', '/ready', '/metrics', '/docs' to backend.",
                 "Verified Pod Status: All pods in 'Running' state in namespace 'bookease' (recorded in docs/k8s_bookease_status.txt).",
                 "Horizontal Pod Autoscaler (HPA v2): Target 70% CPU; Range: 2 to 5 replicas.",
                 "Live Stress Test Verification: Simulated 35 concurrent workers hammering /api/doctors surged CPU to 240%, automatically scaling backend pods from 2 to 5 replicas.",
                 "Cool-down Recovery: Pods returned to 2 replicas after load ceased."
             ])

    s10.notes_slide.notes_text_frame.text = (
        "For M8, our Helm chart manages the entire application. We verified multi-replica deployments, "
        "persistent storage for PostgreSQL, Ingress traffic routing, and live Horizontal Pod Autoscaling under stress."
    )

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 11: M9 — Observability (Prometheus + Grafana)
    # ─────────────────────────────────────────────────────────────────────────
    s11 = prs.slides.add_slide(blank_layout)
    bg11 = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg11.fill.solid()
    bg11.fill.fore_color.rgb = BG_DARK
    bg11.line.fill.background()
    add_header(s11, "Module M9: Full-Stack Observability & Metrics")

    add_card(s11, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Prometheus Metric Collection", [
                 "Backend Instrumentation: Prometheus FastAPI Instrumentator exposing request metrics at /metrics.",
                 "Scrape Configuration: Prometheus scrapes bookease-backend-pods every 10 seconds in namespace 'monitoring'.",
                 "Target Health: Target 'bookease-backend' verified in state UP (1/1 endpoints active).",
                 "Raw Evidence: Captured in docs/metrics_output.txt and docs/screenshots/prometheus_targets_up.png.",
                 "Cluster Metrics: Integrated with Kube State Metrics for pod & node tracking."
             ])

    add_card(s11, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "Populated Grafana Dashboard", [
                 "Automated Provisioning: Custom BookEase dashboard JSON loaded via ConfigMap into Grafana.",
                 "Live Panel 1: Active Backend Replicas (live pod count).",
                 "Live Panel 2: Total Requests Served (>6,600 recorded during testing).",
                 "Live Panel 3: HTTP Error Rate % (gauge).",
                 "Live Panel 4: Request Latency p95 and p99 histograms.",
                 "Live Panel 5: Throughput by endpoint (req/s).",
                 "Live Panel 6: Process CPU & Memory RSS consumption.",
                 "Screenshot Evidence: docs/screenshots/grafana_bookease_dashboard.png."
             ])

    s11.notes_slide.notes_text_frame.text = (
        "Module M9 demonstrates end-to-end observability. The FastAPI backend exposes Prometheus metrics, "
        "Prometheus scrapes all backend pods, and Grafana displays 6 live panels capturing request rates, "
        "latency, and resource utilization."
    )

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 12: M10 — Rubric Compliance & Evidence Audit
    # ─────────────────────────────────────────────────────────────────────────
    s12 = prs.slides.add_slide(blank_layout)
    bg12 = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg12.fill.solid()
    bg12.fill.fore_color.rgb = BG_DARK
    bg12.line.fill.background()
    add_header(s12, "Module M10: 100-Point Rubric Verification & Evidence")

    add_card(s12, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Rubric Verification Scorecard", [
                 "M1 App & DB (10 pts): PASS (10/10) — FastAPI, React, Postgres, Alembic.",
                 "M2 Pytest (10 pts): PASS (10/10) — 16 unit tests, SQLite isolation.",
                 "M3 Git/GitHub (5 pts): PASS (5/5) — Public repo, 12+ commits, clean .gitignore.",
                 "M4 Docker (10 pts): PASS (10/10) — Multi-stage, non-root, Compose stack.",
                 "M5 CI/CD (15 pts): PASS (15/15) — Actions pipeline, GHCR, SHA tags.",
                 "M6 Trivy (5 pts): PASS (5/5) — 0 High/Critical CVEs, gate enforced.",
                 "M7 Terraform (15 pts): PARTIAL (5/15) — Valid HCL, EKS 1.34, provider init. (10 pts cloud apply deferred for cost control).",
                 "M8 K8s & Helm (15 pts): PASS (15/15) — Helm release, Ingress, HPA 2→5.",
                 "M9 Observability (10 pts): PASS (10/10) — Prometheus UP, Grafana panels.",
                 "M10 Docs & Demo (5 pts): PASS (5/5) — README, DEMO.md, presentation."
             ])

    add_card(s12, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "Audited Evidence Artifacts", [
                 "docs/screenshots/bookease_dashboard.png — Live SPA UI",
                 "docs/screenshots/appointments_page.png — Booking Table",
                 "docs/screenshots/doctors_page.png — Doctor Management",
                 "docs/screenshots/ingress_application.png — Ingress Access",
                 "docs/screenshots/prometheus_targets_up.png — Scrape State UP",
                 "docs/screenshots/grafana_bookease_dashboard.png — Live Metrics",
                 "docs/metrics_output.txt — Raw Prometheus scrape",
                 "docs/pytest_output.txt — 16/16 Passed test log",
                 "docs/k8s_bookease_status.txt — Pods & Services status",
                 "docs/FINAL_AUDIT.md — Complete rubric audit log"
             ])

    s12.notes_slide.notes_text_frame.text = (
        "This scorecard summarizes our verified performance. 90 out of 100 points are fully verified "
        "with reproducible logs and screenshots. M7 Terraform code is 100% valid and verified offline, "
        "with live cloud apply safely paused to prevent unnecessary student expenses."
    )

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 13: Limitations & Production Roadmap
    # ─────────────────────────────────────────────────────────────────────────
    s13 = prs.slides.add_slide(blank_layout)
    bg13 = s13.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg13.fill.solid()
    bg13.fill.fore_color.rgb = BG_DARK
    bg13.line.fill.background()
    add_header(s13, "Honest Engineering: Limitations & Production Roadmap")

    add_card(s13, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Current Capstone Constraints", [
                 "In-Cluster PostgreSQL: Database runs inside Kubernetes with PVC; suitable for development and demo, but single point of failure.",
                 "Plain HTTP Ingress: Traffic routed over HTTP port 80; requires custom domain and cert-manager / ACM for production HTTPS.",
                 "Local Secret Values: Basic Kubernetes Secret used; credentials passed via values file rather than dynamic KMS / Secrets Manager.",
                 "Controlled Cloud Spend: Terraform infrastructure validated offline ($0 spend) rather than keeping live AWS instances billing.",
                 "Manual Helm Invocation: CI builds and pushes images; deployment triggered via Helm CLI rather than automated GitOps pull."
             ])

    add_card(s13, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "Production Evolution Roadmap", [
                 "Managed Cloud Database: Transition from in-cluster Postgres to Amazon RDS PostgreSQL Multi-AZ with automated backups and read replicas.",
                 "AWS Secrets Manager Integration: Deploy External Secrets Operator (ESO) with IAM Roles for Service Accounts (IRSA).",
                 "End-to-End TLS / HTTPS: Configure AWS Certificate Manager (ACM) with AWS Load Balancer Controller for automated TLS termination.",
                 "GitOps Automation: Introduce Argo CD or Flux for declarative, pull-based continuous deployment and drift detection.",
                 "Centralized Distributed Tracing: Add OpenTelemetry instrumentation and AWS CloudWatch / Grafana Tempo for distributed tracing."
             ])

    s13.notes_slide.notes_text_frame.text = (
        "True engineering maturity involves recognizing system limitations. In a high-traffic production "
        "environment, we would migrate Postgres to Amazon RDS Multi-AZ, terminate TLS via ACM, "
        "and introduce External Secrets Operator with AWS Secrets Manager."
    )

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 14: Conclusion & Q&A
    # ─────────────────────────────────────────────────────────────────────────
    s14 = prs.slides.add_slide(blank_layout)
    bg14 = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg14.fill.solid()
    bg14.fill.fore_color.rgb = BG_DARK
    bg14.line.fill.background()

    tb14 = s14.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.333), Inches(4.0))
    tf14 = tb14.text_frame
    tf14.word_wrap = True

    p14_badge = tf14.paragraphs[0]
    p14_badge.text = "CONCLUSION & SUBMISSION SUMMARY"
    p14_badge.font.size = Pt(13)
    p14_badge.font.bold = True
    p14_badge.font.color.rgb = ACCENT_CYAN
    p14_badge.space_after = Pt(14)

    p14_title = tf14.add_paragraph()
    p14_title.text = "Thank You! Questions & Discussion"
    p14_title.font.size = Pt(36)
    p14_title.font.bold = True
    p14_title.font.color.rgb = TEXT_WHITE
    p14_title.space_after = Pt(16)

    p14_points = tf14.add_paragraph()
    p14_points.text = (
        "• All 10 Capstone Modules engineered, tested, and documented with verifiable evidence.\n"
        "• 16 Pytest tests, 0 Trivy CVEs, SHA-tagged GHCR images, and automated Alembic migrations.\n"
        "• Kubernetes Helm deployment proven live with Ingress, HPA autoscaling (2→5), and Prometheus/Grafana.\n"
        "• AWS Terraform IaC validated offline and cost-optimized for EKS Standard Support v1.34.\n"
        "• Repository: https://github.com/Durgaprasad-Developer/session21-devops-capstone-final"
    )
    p14_points.font.size = Pt(15)
    p14_points.font.color.rgb = TEXT_MUTED
    p14_points.space_after = Pt(24)

    s14.notes_slide.notes_text_frame.text = (
        "Thank you for evaluating BookEase. I am now open to your questions regarding any aspect of the "
        "application architecture, CI/CD pipeline, Kubernetes deployment, or AWS Terraform design."
    )

    # Save presentation to all specified output paths
    for path in output_paths:
        prs.save(path)
        print(f"Presentation saved to: {path}")

if __name__ == "__main__":
    paths = [
        "docs/presentation/BookEase_DevOps_Capstone_Presentation.pptx",
        "demo/BookEase_DevOps_Capstone_Presentation.pptx"
    ]
    create_deck(paths)
