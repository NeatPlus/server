# Create random id for using as suffix in resource name
resource "random_id" "resource_suffix" {
  byte_length = 4
}

# Generate random username for RDS
resource "random_string" "rds" {
  count = var.rds_username == null ? 1 : 0

  length  = 12
  special = false
  upper   = true
}

# Generate random password for RDS
resource "random_password" "rds" {
  count = var.rds_password == null ? 1 : 0

  length  = 12
  special = false
  upper   = true
}

# Generate random password for RDS
resource "random_password" "redis" {
  count = var.redis_password == null ? 1 : 0

  length  = 12
  special = false
  upper   = true
}
