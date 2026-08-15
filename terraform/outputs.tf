output "ecr_repository_url" {
  value       = aws_ecr_repository.secure_api_repo.repository_url
  description = "The URL of the created Amazon ECR repository"
}

output "ecs_cluster_name" {
  value       = aws_ecs_cluster.app_cluster.name
  description = "The name of the ECS cluster"
}

output "ecs_service_name" {
  value       = aws_ecs_service.app_service.name
  description = "The name of the ECS service"
}