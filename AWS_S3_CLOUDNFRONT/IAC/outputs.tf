output "bucket_name" {
  description = "The name of the S3 bucket"
  value       = aws_s3_bucket.bucket.id
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket"
  value       = aws_s3_bucket.bucket.arn
}

output "bucket_domain" {
  description = "bucket domain endpoint"
  value       = aws_s3_bucket_website_configuration.website.website_endpoint
}

output "hosted_zone_id" {
  description = "bucket domain endpoint"
  value       = aws_s3_bucket.bucket.hosted_zone_id
}

output "www_domain" {
  description = "The www domain name"
  value       = aws_route53_record.www.name
}

output "root_domain" {
  description = "The root domain name"
  value       = aws_route53_record.root.name
}
