variable "aws_region" {
  type        = string
  description = "The AWS region where resources will be created"
  default     = "us-east-1"
}

variable "app_name" {
  type        = string
  description = "The application name used across resource naming"
  default     = "secure-pipeline-api"
}

variable "environment" {
  type        = string
  description = "The deployment environment (Dev, Staging, Prod)"
  default     = "Dev"
}

variable "container_port" {
  type        = number
  description = "The port exposed by the Flask application container"
  default     = 5000
}