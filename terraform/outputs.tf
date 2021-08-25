output "cluster_name" {
  value       = local.cluster_name
  description = "Name of cluster"
}

output "rds_username" {
  value       = local.rds_username
  sensitive   = true
  description = "Username for RDS database"
}

output "rds_password" {
  value       = local.rds_password
  sensitive   = true
  description = "Password for database"
}

output "redis_password" {
  value       = local.redis_password
  sensitive   = true
  description = "Password for redis"
}

output "rds_address" {
  value       = aws_db_instance.postgresql.address
  description = "Address of RDS"
}

output "redis_address" {
  value       = aws_elasticache_replication_group.redis.primary_endpoint_address
  description = "Address of redis"
}

output "s3_bucket_name" {
  value       = aws_s3_bucket.storage.bucket
  description = "Name of s3 bucket"
}
