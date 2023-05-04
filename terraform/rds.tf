# RDS db subnet group
resource "aws_db_subnet_group" "main" {
  name       = "postgresql-${local.suffix}"
  subnet_ids = local.rds_private_subnet_id_list

  tags = {
    "Name" = "postgresql-${local.suffix}"
  }
}

# Security group for RDS
resource "aws_security_group" "rds" {
  name   = "postgresql-${local.suffix}"
  vpc_id = aws_vpc.main.id

  tags = {
    "Name" = "postgresql-${local.suffix}"
  }
}

# RDS ingress security group rule for self
resource "aws_security_group_rule" "rds_private_ingress" {
  type              = "ingress"
  from_port         = var.rds_port
  to_port           = var.rds_port
  protocol          = "tcp"
  self              = true
  security_group_id = aws_security_group.rds.id
}

# RDS ingress security group rule for node of eks
resource "aws_security_group_rule" "rds_eks_ingress" {
  type              = "ingress"
  from_port         = var.rds_port
  to_port           = var.rds_port
  protocol          = "tcp"
  cidr_blocks       = concat(local.eks_public_subnet_cidr_list, local.eks_private_subnet_cidr_list)
  security_group_id = aws_security_group.rds.id
}

# RDS egress security group rule for self
resource "aws_security_group_rule" "rds_private_egress" {
  type              = "egress"
  from_port         = 0
  to_port           = 65535
  protocol          = "tcp"
  self              = true
  security_group_id = aws_security_group.rds.id
}

# RDS egress security group rule for node of eks
resource "aws_security_group_rule" "rds_eks_egress" {
  type              = "egress"
  from_port         = 0
  to_port           = 65535
  protocol          = "tcp"
  cidr_blocks       = concat(local.eks_public_subnet_cidr_list, local.eks_private_subnet_cidr_list)
  security_group_id = aws_security_group.rds.id
}

# create RDS DB instance
resource "aws_db_instance" "postgresql" {
  allocated_storage                   = 50
  auto_minor_version_upgrade          = true
  backup_retention_period             = 7
  backup_window                       = "03:00-04:00"
  db_name                             = var.rds_database_name
  db_subnet_group_name                = aws_db_subnet_group.main.id
  delete_automated_backups            = true
  engine                              = "postgres"
  final_snapshot_identifier           = "postgresql-final-snapshot-${time_static.current.unix}-${local.suffix}"
  iam_database_authentication_enabled = false
  identifier                          = "postgres-${local.suffix}"
  instance_class                      = var.rds_instance_class
  maintenance_window                  = "Sat:00:00-Sat:02:00"
  max_allocated_storage               = 100
  multi_az                            = false
  parameter_group_name                = "default.postgres13"
  password                            = local.rds_password
  port                                = var.rds_port
  publicly_accessible                 = false
  skip_final_snapshot                 = false
  storage_encrypted                   = true
  storage_type                        = "gp2"
  username                            = local.rds_username
  vpc_security_group_ids              = [aws_security_group.rds.id]

  tags = {
    "Name" = "postgresql-${local.suffix}"
  }
}
