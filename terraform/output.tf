output "sqs_queue_arn" {
  value = aws_sqs_queue.sqs_queue_test.arn
}

output "sqs_queue_url" {
  value = aws_sqs_queue.sqs_queue_test.url
}
