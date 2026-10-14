# BookEase — AWS Infrastructure as Code (Terraform)

This directory contains the production-grade, cost-optimized Terraform configuration to provision the AWS cloud infrastructure for BookEase in region `ap-south-1` (Mumbai).

## Architecture Overview

```
AWS Cloud (ap-south-1 — Mumbai)
└── VPC (10.0.0.0/16)
    ├── Internet Gateway
    ├── Public Subnets (2 AZs)
    │   ├── ap-south-1a (10.0.1.0/24) — NAT Gateway + ALB Ingress
    │   └── ap-south-1b (10.0.2.0/24) — ALB Ingress (High Availability)
    ├── Single NAT Gateway (Cost-optimized classroom architecture)
    └── Private Subnets (2 AZs)
        ├── ap-south-1a (10.0.10.0/24) — EKS Managed Node Group
        └── ap-south-1b (10.0.20.0/24) — EKS Managed Node Group
```

### Key Components

- **Amazon VPC**: Custom CIDR `10.0.0.0/16` with DNS hostnames and support enabled.
- **Subnets**: 2 Public subnets and 2 Private subnets distributed across `ap-south-1a` and `ap-south-1b`.
  - Public subnets tagged with `kubernetes.io/role/elb = 1`.
  - Private subnets tagged with `kubernetes.io/role/internal-elb = 1`.
- **Egress Architecture**: Internet Gateway for public traffic and a single cost-optimized NAT Gateway for private node egress.
- **Amazon EKS Cluster**: Kubernetes v1.34 control plane (AWS Standard Support) with private and public API endpoint access.
- **Managed Node Group**: 2x `t3.medium` instances (scaling 1–4) running Amazon Linux 2 / Bottlerocket with 20 GiB gp3 root volumes.
- **IAM Roles & Policies**: Dedicated least-privilege IAM roles for EKS Control Plane (`AmazonEKSClusterPolicy`, `AmazonEKSVPCResourceController`) and Worker Nodes (`AmazonEKSWorkerNodePolicy`, `AmazonEKS_CNI_Policy`, `AmazonEC2ContainerRegistryReadOnly`).
- **Security Groups**: Granular control plane and node communication rules.

---

## Cost Analysis & Main Cost Drivers

To prevent unexpected AWS charges, here is a breakdown of estimated monthly costs in `ap-south-1`:

| Resource | Quantity & Tier | Estimated Cost (ap-south-1) |
|---|---|---|
| **EKS Control Plane** | 1 cluster | ~$0.10 / hour (~$73.00 / month) |
| **EC2 Worker Nodes** | 2x `t3.medium` (2 vCPU, 4 GiB) | ~$0.0416 / hr × 2 (~$60.00 / month) |
| **NAT Gateway** | 1 gateway + data processing | ~$0.045 / hr (~$32.40 / month + data) |
| **EBS Storage** | 2x 20 GiB gp3 root disks | ~$3.20 / month |
| **Total Estimated Cost** | Active Cluster | **~$168.00 / month (~$5.60 / day)** |

> [!TIP]
> **Cost Optimization**:
> - Never leave the cluster running indefinitely after project evaluation.
> - Run `terraform destroy` when not actively conducting tests.

---

## Prerequisites

1. **AWS CLI v2** installed and configured:
   ```bash
   aws configure
   aws sts get-caller-identity
   ```
2. **Terraform** (>= 1.5.0):
   ```bash
   terraform -version
   ```
3. **kubectl**:
   ```bash
   kubectl version --client
   ```

---

## Deployment Steps

### 1. Initialize Terraform
```bash
cd terraform
terraform init
```

### 2. Validate Configuration
```bash
terraform fmt -check -recursive
terraform validate
```

### 3. Review Plan
```bash
terraform plan -out=tfplan
```
*Carefully review the proposed changes before proceeding to apply.*

### 4. Apply (Provision Infrastructure)
```bash
terraform apply tfplan
```
*Provisioning an EKS cluster and managed node group typically takes 10 to 15 minutes.*

### 5. Configure Local `kubectl`
Once `apply` finishes, configure your local kubeconfig using the output command:
```bash
aws eks update-kubeconfig --region ap-south-1 --name bookease-eks-cluster
kubectl get nodes
```

---

## Teardown & Cleanup

To avoid ongoing AWS charges, destroy the infrastructure immediately after completing grading or testing:

```bash
cd terraform
terraform destroy -auto-approve
```

> [!WARNING]
> Before running `terraform destroy`, ensure any Kubernetes LoadBalancer services or PVCs created by Helm have been removed (`helm uninstall ...`), otherwise associated ALBs/ELBs may block VPC deletion.
