# Network ACL for EKS public 
resource "aws_network_acl" "eks_public" {
  vpc_id     = aws_vpc.main.id
  subnet_ids = local.eks_public_subnet_id_list

  tags = {
    Name = "eks-public-${local.suffix}"
  }
}

# EKS public network acl rule to allow all ingress
resource "aws_network_acl_rule" "eks_public_ingress" {
  network_acl_id = aws_network_acl.eks_public.id
  rule_number    = 100
  egress         = false
  protocol       = "-1"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 0
  to_port        = 0
}

# EKS public network acl rule to allow all egress
resource "aws_network_acl_rule" "eks_public_egress" {
  network_acl_id = aws_network_acl.eks_public.id
  rule_number    = 200
  egress         = true
  protocol       = "-1"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 0
  to_port        = 0
}

# Network ACL for EKS private 
resource "aws_network_acl" "eks_private" {
  vpc_id     = aws_vpc.main.id
  subnet_ids = local.eks_private_subnet_id_list

  tags = {
    Name = "eks-private-${local.suffix}"
  }
}

# EKS private network acl rule to allow all ingress
resource "aws_network_acl_rule" "eks_private_ingress" {
  network_acl_id = aws_network_acl.eks_private.id
  rule_number    = 100
  egress         = false
  protocol       = "-1"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 0
  to_port        = 65535
}

# EKS private network acl rule to allow all egress
resource "aws_network_acl_rule" "eks_private_egress" {
  network_acl_id = aws_network_acl.eks_private.id
  rule_number    = 200
  egress         = true
  protocol       = "-1"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 0
  to_port        = 65535
}


# Network ACL for RDS private 
resource "aws_network_acl" "rds_private" {
  vpc_id     = aws_vpc.main.id
  subnet_ids = local.rds_private_subnet_id_list

  tags = {
    Name = "rds-private-${local.suffix}"
  }
}

# RDS private network acl rule to allow rds port ingress to EKS private subnet
resource "aws_network_acl_rule" "rds_acl_eks_private_ingress" {
  for_each = var.eks_private_subnet

  network_acl_id = aws_network_acl.rds_private.id
  rule_number    = sum([100, each.value.priority])
  egress         = false
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = each.value.cidr_block
  from_port      = var.rds_port
  to_port        = var.rds_port
}

# RDS private network acl rule to allow all port ingress to RDS private subnet
resource "aws_network_acl_rule" "rds_acl_rds_private_ingress" {
  for_each = var.rds_private_subnet

  network_acl_id = aws_network_acl.rds_private.id
  rule_number    = sum([200, each.value.priority])
  egress         = false
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = each.value.cidr_block
  from_port      = 0
  to_port        = 65535
}

# RDS private network acl rule to allow egress to RDS and EKS private subnet
resource "aws_network_acl_rule" "rds_acl_egress" {
  for_each = merge(var.eks_private_subnet, var.rds_private_subnet)

  network_acl_id = aws_network_acl.rds_private.id
  rule_number    = sum([300, each.value.priority])
  egress         = true
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = each.value.cidr_block
  from_port      = 0
  to_port        = 65535
}


# Network ACL for redis private 
resource "aws_network_acl" "redis_private" {
  vpc_id     = aws_vpc.main.id
  subnet_ids = local.redis_private_subnet_id_list

  tags = {
    Name = "redis-private-${local.suffix}"
  }
}

# redis private network acl rule to allow redis port ingress to EKS private subnet
resource "aws_network_acl_rule" "redis_acl_eks_private_ingress" {
  for_each = var.eks_private_subnet

  network_acl_id = aws_network_acl.redis_private.id
  rule_number    = sum([100, each.value.priority])
  egress         = false
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = each.value.cidr_block
  from_port      = var.redis_port
  to_port        = var.redis_port
}

# redis private network acl rule to allow all port ingress to redis private subnet
resource "aws_network_acl_rule" "redis_acl_redis_private_ingress" {
  for_each = var.redis_private_subnet

  network_acl_id = aws_network_acl.redis_private.id
  rule_number    = sum([200, each.value.priority])
  egress         = false
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = each.value.cidr_block
  from_port      = 0
  to_port        = 65535
}

# redis private network acl rule to allow egress to redis and EKS private subnet
resource "aws_network_acl_rule" "redis_acl_egress" {
  for_each = merge(var.eks_private_subnet, var.redis_private_subnet)

  network_acl_id = aws_network_acl.redis_private.id
  rule_number    = sum([300, each.value.priority])
  egress         = true
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = each.value.cidr_block
  from_port      = 0
  to_port        = 65535
}

