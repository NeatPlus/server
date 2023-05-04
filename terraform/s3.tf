# Create AWS VPC endpoint for s3 service
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = aws_vpc.main.id
  service_name      = "com.amazonaws.${var.region}.s3"
  vpc_endpoint_type = "Gateway"

  tags = {
    "Name" = "s3-vpc-endpoint-${local.suffix}"
  }
}

# Manages a S3 VPC Endpoint and public Route Table Association
resource "aws_vpc_endpoint_route_table_association" "public" {
  route_table_id  = aws_route_table.public.id
  vpc_endpoint_id = aws_vpc_endpoint.s3.id
}


# Manages a S3 VPC Endpoint and private Route Table Association
resource "aws_vpc_endpoint_route_table_association" "private" {
  for_each        = var.eks_public_subnet
  route_table_id  = aws_route_table.private[each.key].id
  vpc_endpoint_id = aws_vpc_endpoint.s3.id
}

# Create s3 bucket
resource "aws_s3_bucket" "storage" {
  bucket = "${var.s3_bucket_name}-${local.suffix}"

  tags = {
    "Name" = "${var.s3_bucket_name}-${local.suffix}"
  }
}

# Create cors configuration
resource "aws_s3_bucket_cors_configuration" "storage" {
  bucket = aws_s3_bucket.storage.id
  cors_rule {
    allowed_methods = ["GET"]
    allowed_origins = ["https://*.neatplus.org", "https://neatplus.org"]
    max_age_seconds = 3600
  }
}

# Create bucket acl
resource "aws_s3_bucket_acl" "storage" {
  bucket = aws_s3_bucket.storage.id
  acl    = "private"
}
