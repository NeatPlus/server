# Create EKS public subnet
resource "aws_subnet" "eks_public" {
  for_each = var.eks_public_subnet

  vpc_id                  = aws_vpc.main.id
  map_public_ip_on_launch = true
  availability_zone       = each.value.az
  cidr_block              = each.value.cidr_block

  tags = {
    Name                                          = "${each.key}-${local.suffix}"
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/elb"                      = "1"
  }
}

# Create EKS private subnet
resource "aws_subnet" "eks_private" {
  for_each = var.eks_private_subnet

  vpc_id                  = aws_vpc.main.id
  map_public_ip_on_launch = false
  availability_zone       = each.value.az
  cidr_block              = each.value.cidr_block

  tags = {
    Name                                          = "${each.key}-${local.suffix}"
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/internal-elb"             = "1"
  }
}

# Create RDS private subnet
resource "aws_subnet" "rds_private" {
  for_each = var.rds_private_subnet

  vpc_id                  = aws_vpc.main.id
  map_public_ip_on_launch = false
  availability_zone       = each.value.az
  cidr_block              = each.value.cidr_block

  tags = {
    Name = "${each.key}-${local.suffix}"
  }
}

# Create redis private subnet
resource "aws_subnet" "redis_private" {
  for_each = var.redis_private_subnet

  vpc_id                  = aws_vpc.main.id
  map_public_ip_on_launch = false
  availability_zone       = each.value.az
  cidr_block              = each.value.cidr_block

  tags = {
    Name = "${each.key}-${local.suffix}"
  }
}

# Association between EKS public subnet and VPC public route table which contains internet gateway route 
resource "aws_route_table_association" "public" {
  for_each = var.eks_public_subnet

  subnet_id      = aws_subnet.eks_public[each.key].id
  route_table_id = aws_route_table.public.id
}


# Association between EKS private subnet and VPC private route table which contains NAT gateway route 
resource "aws_route_table_association" "private" {
  for_each = var.eks_private_subnet

  subnet_id      = aws_subnet.eks_private[each.key].id
  route_table_id = aws_route_table.private[each.value.associated_public].id
}
