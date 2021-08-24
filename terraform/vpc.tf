#Create VPC
resource "aws_vpc" "main" {
  cidr_block           = var.cidr_block
  instance_tenancy     = "default"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name                                          = "main-${local.suffix}"
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
  }
}

# Create public route table for VPC
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  tags = {
    "Name" = "public-${local.suffix}"
  }
}

# Create private route table for VPC
resource "aws_route_table" "private" {
  for_each = var.eks_public_subnet

  vpc_id = aws_vpc.main.id
  tags = {
    "Name" = "private--${each.key}-${local.suffix}"
  }
}
