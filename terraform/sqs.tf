resource "aws_sqs_queue" "sqs_queue_test" {
  name = "aws-xray-lambda-segment-shim-queue"
}

resource "aws_lambda_event_source_mapping" "sqs_queue_test" {
  event_source_arn = aws_sqs_queue.sqs_queue_test.arn
  function_name    = aws_lambda_function.test_lambda.arn
}
