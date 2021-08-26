# EKS IAM role
resource "aws_iam_role" "eks" {
  name               = local.cluster_name
  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY

  tags = {
    "Name" = local.cluster_name
  }
}

# IAM role atatchment for Amazon EKS cluster policy
resource "aws_iam_role_policy_attachment" "eks-AmazonEKSClusterPolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks.name
}

# IAM role atatchment for Amazon EKS service policy
resource "aws_iam_role_policy_attachment" "eks-AmazonEKSServicePolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
  role       = aws_iam_role.eks.name
}


# IAM role atatchment for VPC pod security group
resource "aws_iam_role_policy_attachment" "eks-AmazonEKSVPCResourceController" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSVPCResourceController"
  role       = aws_iam_role.eks.name
}


# Create EKS cluster security group
resource "aws_security_group" "eks" {
  name   = "${local.cluster_name}/ControlPlaneSecurityGroup"
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "${local.cluster_name}/ControlPlaneSecurityGroup"
  }
}

# EKS egress security group rule
resource "aws_security_group_rule" "eks_egress_rule" {
  type              = "egress"
  from_port         = 0
  to_port           = 65535
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.eks.id
}

# Allow nodes to communicate with control plane
resource "aws_security_group_rule" "eks_ingress_rule" {
  type                     = "ingress"
  from_port                = 0
  to_port                  = 65535
  protocol                 = "-1"
  source_security_group_id = aws_security_group.eks_nodes.id
  security_group_id        = aws_security_group.eks.id
}

# Create EKS cluster
resource "aws_eks_cluster" "eks" {
  name     = local.cluster_name
  role_arn = aws_iam_role.eks.arn
  version  = var.eks_cluster_version

  vpc_config {
    endpoint_private_access = false
    endpoint_public_access  = true
    public_access_cidrs     = ["0.0.0.0/0"]
    security_group_ids      = [aws_security_group.eks.id]
    subnet_ids              = concat(local.eks_public_subnet_id_list, local.eks_private_subnet_id_list)
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks-AmazonEKSClusterPolicy,
    aws_iam_role_policy_attachment.eks-AmazonEKSVPCResourceController,
    aws_iam_role_policy_attachment.eks-AmazonEKSServicePolicy
  ]

  tags = {
    "Name" = local.cluster_name
  }
}
