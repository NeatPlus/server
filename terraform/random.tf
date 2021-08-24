# Create random id for using as suffix in resource name
resource "random_id" "resource_suffix" {
  byte_length = 4
}

# Generate random username for RDS
resource "random_string" "rds" {
  length  = 12
  special = false
  upper   = true
}

# Generate random password for RDS
resource "random_password" "rds" {
  length           = 12
  special          = true
  upper            = true
  override_special = "!#$&*()-_"
}

# Generate random password for RDS
resource "random_password" "redis" {
  length           = 12
  special          = true
  upper            = true
  override_special = "!#$&*()-_"
}
