resource "aws_s3_bucket" "aaiTerraformStateS3Bucket" {
  bucket = "aai-terraform-state-do-not-delete"
}

resource "aws_s3_bucket_versioning" "aaiTerraformStateS3Bucket" {
  bucket = aws_s3_bucket.aaiTerraformStateS3Bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "aaiTerraformStateS3Bucket" {
  bucket = aws_s3_bucket.aaiTerraformStateS3Bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "AES256"
    }
  }
}

resource "aws_s3_bucket_acl" "aaiTerraformStateS3Bucket" {
  bucket = aws_s3_bucket.aaiTerraformStateS3Bucket.id
  acl    = "private"
}

resource "aws_s3_bucket_public_access_block" "aaiTerraformStateS3Bucket" {
  bucket = aws_s3_bucket.aaiTerraformStateS3Bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_dynamodb_table" "aaiDynamodbTerraformLock" {
  name           = "aai-terraform-lock"
  hash_key       = "LockID"
  read_capacity  = 20
  write_capacity = 20
#   billing_mode = "PAY_PER_REQUEST"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    name = "AAI Terraform Lock Table"
  }
}
