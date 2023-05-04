# Cloudwatch log group for alarm
resource "aws_sns_topic" "alarms" {
  name = "${var.project_name}-${local.suffix}-alarms-sns-topic"
}

resource "aws_sqs_queue" "alarms_queue" {
  name = "${var.project_name}-${local.suffix}-alarms-queue"
}

resource "aws_sns_topic_subscription" "alarms_sqs_target" {
  topic_arn = aws_sns_topic.alarms.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.alarms_queue.arn
}
module "cis_alarms" {
  source  = "terraform-aws-modules/cloudwatch/aws//modules/cis-alarms"
  version = "4.2.1"

  alarm_actions          = [aws_sns_topic.alarms.arn]
  log_group_name         = "aws-cloudtrail-logs"
  use_random_name_prefix = true
}
