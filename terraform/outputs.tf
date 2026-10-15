output "aws_region" {
  description = "Configured AWS region"
  value       = var.aws_region
}

output "vpc_id" {
  description = "ID of the BookEase VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr_block" {
  description = "CIDR block of the BookEase VPC"
  value       = aws_vpc.main.cidr_block
}

output "public_subnet_ids" {
  description = "List of public subnet IDs (for ALBs and Ingress)"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "List of private subnet IDs (for EKS Worker Nodes)"
  value       = aws_subnet.private[*].id
}

output "nat_gateway_ip" {
  description = "Public Elastic IP address of the NAT Gateway"
  value       = try(aws_eip.nat[0].public_ip, "Disabled")
}

output "cluster_name" {
  description = "Name of the provisioned Amazon EKS cluster"
  value       = aws_eks_cluster.main.name
}

output "cluster_version" {
  description = "Kubernetes control plane version of the EKS cluster"
  value       = aws_eks_cluster.main.version
}

output "cluster_endpoint" {
  description = "Endpoint URL for the Amazon EKS control plane API"
  value       = aws_eks_cluster.main.endpoint
}

output "cluster_security_group_id" {
  description = "Security group ID attached to the EKS cluster control plane"
  value       = aws_security_group.cluster.id
}

output "node_group_name" {
  description = "Name of the managed worker node group"
  value       = aws_eks_node_group.main.node_group_name
}

output "node_group_status" {
  description = "Status of the managed node group"
  value       = aws_eks_node_group.main.status
}

output "configure_kubectl" {
  description = "Run this AWS CLI command to configure local kubectl to connect to the cluster"
  value       = "aws eks update-kubeconfig --region ${var.aws_region} --name ${aws_eks_cluster.main.name}"
}
