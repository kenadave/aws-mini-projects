# Multi-Region CloudFormation Deployment Instructions

## Overview
This setup creates a Route53 hosted zone, Application Load Balancer, and EC2 instances across multiple regions with DNS failover/load balancing.

## Files Created
1. `cloudformation-multi-region-setup.yaml` - Primary region template
2. `cloudformation-secondary-region.yaml` - Secondary region template

## Deployment Steps

### Step 1: Deploy Primary Region
```bash
aws cloudformation create-stack \
  --stack-name multi-region-primary \
  --template-body file://cloudformation-multi-region-setup.yaml \
  --parameters ParameterKey=DomainName,ParameterValue=yourdomain.com \
               ParameterKey=KeyPairName,ParameterValue=your-key-pair \
  --region us-east-1
```

### Step 2: Get Hosted Zone ID
```bash
aws cloudformation describe-stacks \
  --stack-name multi-region-primary \
  --query 'Stacks[0].Outputs[?OutputKey==`HostedZoneId`].OutputValue' \
  --output text \
  --region us-east-1
```

### Step 3: Deploy Secondary Region
```bash
aws cloudformation create-stack \
  --stack-name multi-region-secondary \
  --template-body file://cloudformation-secondary-region.yaml \
  --parameters ParameterKey=DomainName,ParameterValue=yourdomain.com \
               ParameterKey=KeyPairName,ParameterValue=your-key-pair \
               ParameterKey=PrimaryHostedZoneId,ParameterValue=HOSTED_ZONE_ID_FROM_STEP_2 \
  --region us-west-2
```

## Important Notes

### AMI IDs
Update the AMI IDs in both templates for your target regions:
- Check AWS documentation for latest Amazon Linux 2 AMI IDs
- Use AWS CLI: `aws ec2 describe-images --owners amazon --filters "Name=name,Values=amzn2-ami-hvm-*" --query 'Images[*].[ImageId,Name]' --region YOUR_REGION`

### Key Pairs
Ensure you have EC2 key pairs created in both regions before deployment.

### DNS Configuration
After deployment:
1. Update your domain's nameservers to use the Route53 hosted zone nameservers
2. The setup uses weighted routing (50/50) between regions
3. Access your application at `http://app.yourdomain.com`

### Security Considerations
- The templates allow SSH access from anywhere (0.0.0.0/0) - restrict this in production
- Consider adding HTTPS/SSL certificates for production use
- Implement proper backup and monitoring strategies

### Cleanup
To delete the stacks:
```bash
aws cloudformation delete-stack --stack-name multi-region-secondary --region us-west-2
aws cloudformation delete-stack --stack-name multi-region-primary --region us-east-1
```

## Architecture Components

### Primary Region (us-east-1)
- Route53 Hosted Zone
- VPC with 2 public subnets
- Application Load Balancer
- 2 EC2 instances in different AZs
- Security groups for ALB and instances

### Secondary Region (us-west-2)
- VPC with 2 public subnets
- Application Load Balancer
- 2 EC2 instances in different AZs
- Weighted DNS record pointing to secondary ALB

### Features
- Auto-scaling ready (target groups configured)
- Health checks enabled
- Cross-region DNS load balancing
- Basic web server setup on instances


Internet Request → Route53 → ALB → Target Group → EC2
                     ↓         ↓        ↓         ↓
                 Hosted Zone  Subnets  Subnets  Subnets
                              ↓        ↓         ↓
                             VPC ← Route Table ← IGW


                    One ALB
                       |
        ┌──────────────┼──────────────┐
        │              │              │
    AZ-1a          AZ-1b          AZ-1c
 (us-east-1a)   (us-east-1b)   (us-east-1c)
        │              │              │
   Subnet-1       Subnet-2       Subnet-3
 (10.0.1.0/24)  (10.0.2.0/24)  (10.0.3.0/24)
        │              │              │
   ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
   │         │    │         │    │         │
 EC2-1a   EC2-1b EC2-2a   EC2-2b EC2-3a   EC2-3b

ALB
├── HTTPListener (port 80) → HTTPTargetGroup
└── HTTPSListener (port 443) → HTTPSTargetGroup
