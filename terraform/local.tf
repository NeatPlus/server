# resources related locals
locals {
  suffix         = random_id.resource_suffix.hex
  cluster_name   = "${var.project_name}-cluster-${local.suffix}"
  log_group_name = "${var.project_name}-server-${local.suffix}-logs"
}

# Locals for listing subnet name
locals {
  eks_public_subnet_id_list    = [for key in keys(var.eks_public_subnet) : aws_subnet.eks_public[key].id]
  eks_private_subnet_id_list   = [for key in keys(var.eks_private_subnet) : aws_subnet.eks_private[key].id]
  rds_private_subnet_id_list   = [for key in keys(var.rds_private_subnet) : aws_subnet.rds_private[key].id]
  redis_private_subnet_id_list = [for key in keys(var.redis_private_subnet) : aws_subnet.redis_private[key].id]
}

# local for listing cidrs
locals {
  eks_public_subnet_cidr_list    = [for value in values(var.eks_public_subnet) : value["cidr_block"]]
  eks_private_subnet_cidr_list   = [for value in values(var.eks_private_subnet) : value["cidr_block"]]
  rds_private_subnet_cidr_list   = [for value in values(var.rds_private_subnet) : value["cidr_block"]]
  redis_private_subnet_cidr_list = [for value in values(var.redis_private_subnet) : value["cidr_block"]]
}

# local for RDS and redis username and password
locals {
  rds_username   = var.rds_username == null ? "user${random_string.rds[0].result}" : var.rds_username
  rds_password   = var.rds_password == null ? "pass${random_password.rds[0].result}" : var.rds_password
  redis_password = var.redis_password == null ? "pass${random_password.redis[0].result}" : var.redis_password
}
