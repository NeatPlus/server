# Elasticache subnet group for redis 
resource "aws_elasticache_subnet_group" "main" {
  name       = "redis-${local.suffix}"
  subnet_ids = local.redis_private_subnet_id_list

  tags = {
    "Name" = "redis-${local.suffix}"
  }
}
# Security group for redis
resource "aws_security_group" "redis" {
  name   = "redis-${local.suffix}"
  vpc_id = aws_vpc.main.id

  tags = {
    "Name" = "redis-${local.suffix}"
  }
}

# redis ingress security group rule for self
resource "aws_security_group_rule" "redis_private_ingress" {
  type              = "ingress"
  from_port         = var.redis_port
  to_port           = var.redis_port
  protocol          = "tcp"
  self              = true
  security_group_id = aws_security_group.redis.id
}

# redis ingress security group rule for node of eks
resource "aws_security_group_rule" "redis_eks_ingress" {
  type              = "ingress"
  from_port         = var.redis_port
  to_port           = var.redis_port
  protocol          = "tcp"
  cidr_blocks       = concat(local.eks_public_subnet_cidr_list, local.eks_private_subnet_cidr_list)
  security_group_id = aws_security_group.redis.id
}

# redis egress security group rule for self
resource "aws_security_group_rule" "redis_private_egress" {
  type              = "egress"
  from_port         = 0
  to_port           = 65535
  protocol          = "tcp"
  self              = true
  security_group_id = aws_security_group.redis.id
}

# redis egress security group rule for node of eks
resource "aws_security_group_rule" "redis_eks_egress" {
  type              = "egress"
  from_port         = 0
  to_port           = 65535
  protocol          = "tcp"
  cidr_blocks       = concat(local.eks_public_subnet_cidr_list, local.eks_private_subnet_cidr_list)
  security_group_id = aws_security_group.redis.id
}

# redis elaticache cluster
resource "aws_elasticache_replication_group" "redis" {
  replication_group_id       = "redis-${local.suffix}"
  description                = "redis cluster managed by terraform"
  auth_token                 = local.redis_password
  auto_minor_version_upgrade = true
  automatic_failover_enabled = false
  engine                     = "redis"
  engine_version             = "6.x"
  final_snapshot_identifier  = "redis-final-snapshot-${time_static.current.unix}-${local.suffix}"
  maintenance_window         = "Sat:00:00-Sat:02:00"
  multi_az_enabled           = false
  node_type                  = var.redis_instance_class
  num_cache_clusters         = 1
  port                       = var.redis_port
  security_group_ids         = [aws_security_group.redis.id]
  snapshot_retention_limit   = 7
  snapshot_window            = "03:00-04:00"
  subnet_group_name          = aws_elasticache_subnet_group.main.name
  transit_encryption_enabled = true

  tags = {
    "Name" = "redis-${local.suffix}"
  }
}
