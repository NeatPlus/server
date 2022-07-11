# Cloudwatch log group for vpc flow log
resource "aws_cloudwatch_log_group" "vpc" {
  name              = "main-${local.suffix}-flow-log"
  retention_in_days = 90
}

# IAM role for VPC flow log
resource "aws_iam_role" "flow_log" {
  name = "main-${local.suffix}-flow-log-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "vpc-flow-logs.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

# IAM role policy for VPC flow log
resource "aws_iam_role_policy" "flow_log" {
  name = "main-${local.suffix}-flow-log-role-policy"
  role = aws_iam_role.flow_log.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

# Create flow log for VPC
resource "aws_flow_log" "main" {
  iam_role_arn         = aws_iam_role.flow_log.arn
  log_destination_type = "cloud-watch-logs"
  log_destination      = aws_cloudwatch_log_group.vpc.arn
  traffic_type         = "ALL"
  vpc_id               = aws_vpc.main.id
}


# Cloudwatch log group for server logs
resource "aws_cloudwatch_log_group" "server" {
  name              = local.log_group_name
  retention_in_days = 90
}
