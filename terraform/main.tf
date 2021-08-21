

data "archive_file" "lambda_zip" {
  type        = "zip"
  output_path = "/tmp/lambda_zip.zip"
  source_dir  = "../"
  excludes    = ["terraform/.terraform/"]

}

resource "aws_lambda_function" "test_lambda" {
  filename         = "/tmp/lambda_zip.zip"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  function_name    = "aws_xray_sqs_lambda_segment_shim"
  role             = aws_iam_role.iam_for_lambda.arn
  handler          = "terraform/handler.lambda_handler"
  runtime          = "python3.9"
  tracing_config {
    mode = "Active"
  }
}

provider "aws" {
  region = "eu-west-1"
}
