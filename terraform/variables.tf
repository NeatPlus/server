variable "project_name" {
  type        = string
  default     = "neatplus"
  description = "Name of project"
}

variable "region" {
  type        = string
  default     = "eu-central-1"
  description = "AWS region name"
}

variable "cidr_block" {
  type        = string
  default     = "10.0.0.0/16"
  description = "VPC CIDR block"
}

variable "eks_public_subnet" {
  type = map(object({
    az         = string
    cidr_block = string
    priority   = number
  }))
  default = {
    "public-eks-1" = {
      az         = "eu-central-1a"
      cidr_block = "10.0.0.0/22"
      priority   = 1
    },
    "public-eks-2" = {
      az         = "eu-central-1b"
      cidr_block = "10.0.4.0/22"
      priority   = 2
    }
  }
  description = "Map of EKS public subnet CIDR and AZ"
}

variable "eks_private_subnet" {
  type = map(object({
    az                = string
    cidr_block        = string
    priority          = number
    associated_public = string
  }))
  default = {
    "private-eks-1" = {
      az                = "eu-central-1a"
      cidr_block        = "10.0.40.0/22"
      priority          = 11
      associated_public = "public-eks-1"
    },
    "private-eks-2" = {
      az                = "eu-central-1b"
      cidr_block        = "10.0.44.0/22"
      priority          = 12
      associated_public = "public-eks-2"
    }
  }
  description = "Map of EKS private subnet CIDR and AZ"
}

variable "rds_private_subnet" {
  type = map(object({
    az         = string
    cidr_block = string
    priority   = number
  }))
  default = {
    "private-rds-1" = {
      az         = "eu-central-1a"
      cidr_block = "10.0.80.0/22"
      priority   = 21
    },
    "private-rds-2" = {
      az         = "eu-central-1b"
      cidr_block = "10.0.84.0/22"
      priority   = 22
    }
  }
  description = "Map of rds private subnet CIDR and AZ"
}

variable "redis_private_subnet" {
  type = map(object({
    az         = string
    cidr_block = string
    priority   = number
  }))
  default = {
    "private-redis-1" = {
      az         = "eu-central-1a"
      cidr_block = "10.0.120.0/22"
      priority   = 31
    },
    "private-redis-2" = {
      az         = "eu-central-1b"
      cidr_block = "10.0.124.0/22"
      priority   = 32
    }
  }
  description = "Map of redis private subnet CIDR and AZ"
}

variable "rds_port" {
  type        = number
  default     = 5432
  description = "Port of RDS serive"
}

variable "redis_port" {
  type        = number
  default     = 6379
  description = "Port of redis serive"
}

variable "eks_private_instance_types" {
  type        = list(string)
  default     = ["t3.medium"]
  description = "Instance types of EKS private"
}

variable "eks_public_instance_types" {
  type        = list(string)
  default     = ["t3.medium"]
  description = "Instance types of EKS public"
}

variable "rds_instance_class" {
  type        = string
  default     = "db.t3.small"
  description = "Instance type of RDS"
}

variable "rds_database_name" {
  type        = string
  default     = "neatplus"
  description = "Name of RDS database"
}

variable "redis_instance_class" {
  type        = string
  default     = "cache.t3.small"
  description = "Instance type of redis"
}

variable "s3_bucket_name" {
  type        = string
  default     = "neatplus-storage"
  description = "S3 bucket name for AWS"
}

variable "eks_cluster_version" {
  type        = string
  default     = "1.21"
  description = "Version of cluster"
}

variable "rds_username" {
  type        = string
  default     = null
  description = "Default RDS username if not provided random will be used"
  sensitive   = true
}

variable "rds_password" {
  type        = string
  default     = null
  description = "Default RDS password if not provided random will be used"
  sensitive   = true
}

variable "redis_password" {
  type        = string
  default     = null
  description = "Default redis password if not provided random will be used"
  sensitive   = true
}
