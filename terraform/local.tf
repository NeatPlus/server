# resources related locals
locals {
  suffix       = random_id.resource_suffix.hex
  cluster_name = "eks-cluster-${local.suffix}"
}

# Locals for listing subnet name
locals {
  eks_public_subnet_id_list    = [for key in keys(var.eks_public_subnet) : aws_subnet.eks_public[key].id]
  eks_private_subnet_id_list   = [for key in keys(var.eks_private_subnet) : aws_subnet.eks_private[key].id]
  rds_private_subnet_id_list   = [for key in keys(var.rds_private_subnet) : aws_subnet.rds_private[key].id]
  redis_private_subnet_id_list = [for key in keys(var.redis_private_subnet) : aws_subnet.redis_private[key].id]
}

locals {
  eks_public_subnet_cidr_list    = [for value in values(var.eks_public_subnet) : value["cidr_block"]]
  eks_private_subnet_cidr_list   = [for value in values(var.eks_private_subnet) : value["cidr_block"]]
  rds_private_subnet_cidr_list   = [for value in values(var.rds_private_subnet) : value["cidr_block"]]
  redis_private_subnet_cidr_list = [for value in values(var.redis_private_subnet) : value["cidr_block"]]
}
