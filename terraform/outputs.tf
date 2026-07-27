output "ecr_repository_url" {
  value       = aws_ecr_repository.secure_api_repo.repository_url
  description = "The URL of the created Amazon ECR repository"
}

output "app_runner_url" {
  value       = "https://${aws_apprunner_service.api_service.service_url}"
  description = "The live HTTPS URL of the secure API dashboard"
}

output "app_runner_service_arn" {
  value       = aws_apprunner_service.api_service.arn
  description = "The ARN of the AWS App Runner service"
}