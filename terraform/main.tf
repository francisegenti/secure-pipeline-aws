resource "aws_ecr_repository" "secure_api_repo" {
  name                 = var.app_name
  image_tag_mutability = "MUTABLE"
  force_delete         = true

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Environment = var.environment
    Project     = "SecurePipeline"
  }
}

resource "aws_iam_role" "app_runner_ecr_role" {
  name = "${var.app_name}-ecr-access-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "build.apprunner.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "app_runner_ecr_policy" {
  role       = aws_iam_role.app_runner_ecr_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
}

resource "aws_apprunner_service" "api_service" {
  service_name = "${var.app_name}-service"

  source_configuration {
    authentication_configuration {
      access_role_arn = aws_iam_role.app_runner_ecr_role.arn
    }

    image_repository {
      image_identifier      = "${aws_ecr_repository.secure_api_repo.repository_url}:latest"
      image_repository_type = "ECR"
      image_configuration {
        port = tostring(var.container_port)
      }
    }
    
    auto_deployments_enabled = true
  }

  tags = {
    Environment = var.environment
    Project     = "SecurePipeline"
  }

  depends_on = [aws_iam_role_policy_attachment.app_runner_ecr_policy]
}