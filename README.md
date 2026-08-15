# Secure Pipeline AWS

A Flask REST API deployed to AWS ECS Fargate through a security-first CI/CD pipeline. Built to demonstrate DevSecOps practices: automated vulnerability scanning, infrastructure security scanning, and short-lived credential authentication — with every security decision documented rather than silently suppressed.

## Architecture

- **Application**: Flask REST API, containerized with Docker, running as a non-root user
- **Compute**: AWS ECS Fargate (serverless containers, no EC2 management)
- **Registry**: Amazon ECR with vulnerability scanning enabled on push
- **Infrastructure as Code**: Terraform, with remote state in S3 (native locking, no DynamoDB table)
- **CI/CD**: GitHub Actions — test, scan, then deploy, in that order, each gating the next
- **Authentication**: GitHub Actions authenticates to AWS via OIDC — no long-lived access keys stored anywhere

## Security pipeline

Every push to `main` runs through three gated stages:

1. **Unit tests** (`pytest`) — must pass before anything else runs
2. **Security scans**:
   - **Trivy** scans the built container image for known CVEs (fails the build on HIGH/CRITICAL)
   - **tfsec** scans the Terraform configuration for infrastructure misconfigurations
3. **Deploy** — only runs if tests and scans both pass. Builds and pushes the image to ECR, applies Terraform, then forces an ECS service redeployment

### Handling unpatchable vulnerabilities

Some CVEs flagged by Trivy have no available fix upstream (verified against the Debian Security Tracker) — these are documented and suppressed in [`.trivyignore`](.trivyignore) with a stated reason for each, rather than silently ignored or left permanently blocking the pipeline. This file is reviewed periodically as upstream patches become available.

## Infrastructure

Terraform provisions:
- ECR repository with image scanning on push
- ECS cluster and Fargate service (2 vCPU-second-scale task, default VPC)
- IAM roles scoped per function: task execution role (logs + ECR pull) and a separate GitHub OIDC deploy role (ECR push, ECS deploy, Terraform state access — no admin-level access)
- CloudWatch log group for container logs
- GitHub OIDC identity provider and federated deploy role

## Running locally

\`\`\`bash
docker build -t secure-pipeline-api .
docker run -p