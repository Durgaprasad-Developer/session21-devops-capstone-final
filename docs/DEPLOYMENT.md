# BookEase — Deployment Guide & Lifecycle Operations

This guide provides extended deployment instructions, cloud migration steps, and teardown procedures for BookEase across local Minikube and AWS EKS.

---

## 1. Local Kubernetes Deployment (Minikube)

### Prerequisites
- Minikube >= v1.33 (running Kubernetes v1.30)
- Helm v3.16+
- kubectl v1.30+

### Setup Commands
```bash
# 1. Start cluster with required resources
minikube start --driver=docker --cpus=4 --memory=8192

# 2. Enable necessary cluster add-ons
minikube addons enable ingress
minikube addons enable metrics-server

# 3. Create bookease namespace
kubectl apply -f k8s/namespace.yaml

# 4. Deploy BookEase application via Helm
helm upgrade --install bookease ./helm/bookease \
  --namespace bookease \
  --create-namespace

# 5. Verify all workloads are running
kubectl get pods,svc,hpa,ingress -n bookease
```

---

## 2. Intended AWS EKS Deployment Workflow

> [!NOTE]
> Per capstone guidelines, live cloud provisioning on AWS was held at $0.00 spend. All Terraform configuration files have been formatted, initialized, and validated offline. The steps below document how BookEase deploys to AWS EKS when a live cloud environment is provisioned.

### Step 1: Provision Infrastructure with Terraform
```bash
cd terraform
terraform init
terraform plan -out=tfplan
terraform apply tfplan
```

### Step 2: Configure `kubectl` for EKS
```bash
aws eks update-kubeconfig --region ap-south-1 --name bookease-eks-cluster
kubectl get nodes
```

### Step 3: Install AWS Load Balancer Controller (Target Architecture)
```bash
# Public subnets are pre-tagged with kubernetes.io/role/elb = 1
helm repo add eks https://aws.github.io/eks-charts
helm repo update
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=bookease-eks-cluster \
  --set serviceAccount.create=true
```

### Step 4: Deploy Application Helm Chart to EKS
```bash
# Deploy using SHA-tagged images published in GHCR
helm upgrade --install bookease ./helm/bookease \
  --namespace bookease \
  --create-namespace \
  --set postgresql.persistence.storageClass="gp3"
```

---

## 3. Extended Cost Estimation & Analysis

Amazon EKS charges a standard cluster fee of $0.10/hour (~$72/month). When clusters run versions past official end-of-standard-support (e.g., Kubernetes v1.30), AWS adds an Extended Support surcharge of $0.50/hour (~$360/month), bringing the control plane to ~$432/month.

### Estimated Monthly Cost Comparison (ap-south-1 Mumbai)

| Component | Standard Support (v1.34 IaC Target) | Extended Support (Deprecated v1.30) |
|---|---|---|
| **EKS Control Plane** | $0.10/hr = ~$72.00/mo | $0.60/hr = ~$432.00/mo |
| **2x t3.medium EC2 Nodes** | ~$0.083/hr = ~$60.00/mo | ~$0.083/hr = ~$60.00/mo |
| **NAT Gateway** | ~$0.045/hr = ~$32.40/mo | ~$0.045/hr = ~$32.40/mo |
| **gp3 EBS Storage (40 GiB)** | ~$3.60/mo | ~$3.60/mo |
| **Estimated Total** | **~$168.00 / month** | **~$528.00 / month** |

*Note: The ~$360/month difference represents avoided AWS Extended Support surcharges on the EKS control plane alone, not guaranteed total infrastructure savings.*

---

## 4. Teardown & Safe Cleanup Instructions

### AWS EKS Clean Teardown
```bash
# 1. Uninstall Helm releases first to release ALBs, ENIs, and PVCs
helm uninstall bookease -n bookease
helm uninstall grafana -n monitoring 2>/dev/null || true
helm uninstall prometheus -n monitoring 2>/dev/null || true

# 2. Destroy Terraform infrastructure cleanly
cd terraform
terraform destroy -auto-approve
```

### Local Environment Cleanup
```bash
# Stop Minikube cluster
minikube stop

# Stop Docker Compose stack
# NOTE: The -v flag removes persistent database volumes and deletes local records.
docker compose down -v
```
