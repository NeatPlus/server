# node group IAM role
resource "aws_iam_role" "node_group" {
  name = "node_group-${local.suffix}"

  assume_role_policy = jsonencode({
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
    Version = "2012-10-17"
  })
}

# IAM policy attachment for AmazonEKSWorkerNodePolicy
resource "aws_iam_role_policy_attachment" "node-group-AmazonEKSWorkerNodePolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.node_group.name
}

# IAM policy attachment for AmazonEKS_CNI_POLICY
resource "aws_iam_role_policy_attachment" "node-group-AmazonEKS_CNI_Policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.node_group.name
}

# IAM policy attachment for AMa
resource "aws_iam_role_policy_attachment" "node-group-AmazonEC2ContainerRegistryReadOnly" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.node_group.name
}

# EKS nodes security group
resource "aws_security_group" "eks_nodes" {
  name   = "${local.cluster_name}/ClusterSharedNodeSecurityGroup"
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${local.cluster_name}/ClusterSharedNodeSecurityGroup"
  }
}

# EKS nodes egress security group rule
resource "aws_security_group_rule" "eks_nodes_egress_rule" {
  type              = "egress"
  from_port         = 0
  to_port           = 65535
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.eks_nodes.id
}

# Allow inter node communication
resource "aws_security_group_rule" "eks_nodes_self_ingress_rule" {
  type              = "ingress"
  from_port         = 0
  to_port           = 65535
  protocol          = "-1"
  self              = true
  security_group_id = aws_security_group.eks_nodes.id
}

# Allow control plane and eks control plane communication
resource "aws_security_group_rule" "eks_nodes_control_plane_ingress_rule" {
  type                     = "ingress"
  from_port                = 0
  to_port                  = 65535
  protocol                 = "-1"
  source_security_group_id = aws_security_group.eks.id
  security_group_id        = aws_security_group.eks_nodes.id
}


# Create private EKS node group
resource "aws_eks_node_group" "node" {
  cluster_name    = aws_eks_cluster.eks.name
  node_group_name = "private-node-group-${local.suffix}"
  node_role_arn   = aws_iam_role.node_group.arn
  subnet_ids      = local.eks_private_subnet_id_list
  instance_types  = var.eks_public_instance_types

  scaling_config {
    desired_size = 2
    max_size     = 2
    min_size     = 2
  }

  depends_on = [
    aws_iam_role_policy_attachment.node-group-AmazonEKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.node-group-AmazonEKS_CNI_Policy,
    aws_iam_role_policy_attachment.node-group-AmazonEC2ContainerRegistryReadOnly,
  ]

  tags = {
    "Name"                                            = "private-node-group-${local.suffix}"
    "k8s.io/cluster-autoscaler/${local.cluster_name}" = "owned"
    "k8s.io/cluster-autoscaler/enabled"               = "TRUE"
  }
}

# Policy for cluster auto scaling
resource "aws_iam_policy" "cluster_auto_scaler" {
  name = "eks-node-group-auto-scaler"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "autoscaling:DescribeAutoScalingGroups",
          "autoscaling:DescribeAutoScalingInstances",
          "autoscaling:DescribeLaunchConfigurations",
          "autoscaling:DescribeTags",
          "autoscaling:SetDesiredCapacity",
          "autoscaling:TerminateInstanceInAutoScalingGroup",
          "ec2:DescribeLaunchTemplateVersions"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

# Attach policy to node group iam role
resource "aws_iam_role_policy_attachment" "cluster_auto_sclaer_policy" {
  policy_arn = aws_iam_policy.cluster_auto_scaler.arn
  role       = aws_iam_role.node_group.name
}
