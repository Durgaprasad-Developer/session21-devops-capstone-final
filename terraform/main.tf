# ── AWS Availability Zones Data Source ─────────────────────────────────────────
data "aws_availability_zones" "available" {
  state = "available"
}

# ── Current Account and Caller Identity ───────────────────────────────────────
data "aws_caller_identity" "current" {}

# ── Local Variables ───────────────────────────────────────────────────────────
locals {
  name_prefix = var.cluster_name
  common_tags = {
    Project     = "BookEase"
    Environment = var.environment
    ManagedBy   = "Terraform"
    Cluster     = var.cluster_name
  }
}
