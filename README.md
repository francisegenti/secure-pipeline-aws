# Secure Pipeline AWS

A Flask REST API deployed to AWS ECS Fargate through a security-first CI/CD pipeline. Built to demonstrate DevSecOps practices: automated vulnerability scanning, infrastructure security scanning, and short-lived credential authentication — with every security decision documented rather than silently suppressed.

## Architecture

- **Application**: Flask REST API, containerized with Docker, running as a non-root user
- **Compute**: AWS ECS Fargate (serverless containers, no EC2 management)
- **Registry**: Amazon ECR with vulnerability scanning enabled on push
- **Infrastructure as Code**: Terraform, with remote state in S3 (native locking, no DynamoDB table)
- **CI/CD**: GitHub Actions — test, scan, then deploy, in that order, each gating the next
- **Authentication**: GitHub Actions authenticates to AWS via OIDC — no long-lived access keys stored anywhere

## Prerequisites

To run or deploy this project yourself, you'll need:

- **AWS account** with credentials configured (`aws configure`)
- **Terraform** >= 1.15.0 (uses S3 native state locking via `use_lockfile`)
- **Docker** (for building and running the container locally)
- **AWS CLI** v2
- An **S3 bucket** for Terraform remote state (create manually before first `terraform init`; see `terraform/backend.tf` for the expected bucket name/key)
- A **GitHub repository** with Actions enabled, if you want the CI/CD pipeline to run — this uses OIDC federated auth, so no AWS access keys need to be stored as GitHub secrets, but the IAM OIDC provider and deploy role (`terraform/oidc.tf`) must be applied first

## Setup

```bash
# 1. Create and harden the S3 state bucket (one-time, adjust bucket name)
aws s3api create-bucket --bucket <your-unique-bucket-name> --region us-east-1
aws s3api put-bucket-versioning --bucket <your-unique-bucket-name> --versioning-configuration Status=Enabled
aws s3api put-bucket-encryption --bucket <your-unique-bucket-name> --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'
aws s3api put-public-access-block --bucket <your-unique-bucket-name> --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

# 2. Update terraform/backend.tf with your bucket name, then initialize
cd terraform
terraform init

# 3. Provision the ECR repo first (needed before an image can be pushed)
terraform apply -target=aws_ecr_repository.secure_api_repo

# 4. Build and push the initial image
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker build -t secure-pipeline-api .
docker tag secure-pipeline-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/secure-pipeline-api:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/secure-pipeline-api:latest

# 5. Provision the rest of the infrastructure (ECS cluster, service, IAM, OIDC trust)
terraform apply
```

## Security pipeline

Every push to `main` runs through three gated stages:

1. **Unit tests** (`pytest`) — must pass before anything else runs
2. **Security scans**:
   - **Trivy** scans the built container image for known CVEs (fails the build on HIGH/CRITICAL severity)
   - **tfsec** scans the Terraform configuration for infrastructure misconfigurations
3. **Deploy** — only runs if tests and scans both pass. Builds and pushes the image to ECR, applies Terraform, then forces an ECS service redeployment so the new image actually goes live

### Handling unpatchable vulnerabilities

Some CVEs flagged by Trivy have no available fix upstream (verified against the Debian Security Tracker, and in a couple of cases confirmed as vendored dependencies of pip itself rather than the application). These are documented and suppressed in [`.trivyignore`](.trivyignore) with a stated reason for each entry, rather than silently ignored or left permanently blocking the pipeline. The file is reviewed periodically as upstream patches become available.

## Infrastructure

Terraform provisions:
- ECR repository with image scanning on push
- ECS cluster and Fargate service, running in the default VPC
- IAM roles scoped per function: a task execution role (CloudWatch logs + ECR pull only) and a separate GitHub OIDC deploy role (ECR push, ECS deploy, Terraform state access — not a blanket admin role)
- CloudWatch log group for container logs
- GitHub OIDC identity provider and federated deploy role, so CI/CD authenticates without storing AWS access keys

## Running locally

```bash
docker build -t secure-pipeline-api .
docker run -p 5000:5000 secure-pipeline-api
curl http://localhost:5000/health
```

## Tech stack

Flask · Docker · Terraform · AWS ECS Fargate · AWS ECR · AWS IAM (OIDC) · GitHub Actions · Trivy · tfsec