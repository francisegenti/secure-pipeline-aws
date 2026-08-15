terraform {
  backend "s3" {
    bucket       = "francisegenti-secure-pipeline-aws-tfstate"
    key          = "secure-pipeline-aws/terraform.tfstate"
    region       = "us-east-1"
    use_lockfile = true
    encrypt      = true
  }
}