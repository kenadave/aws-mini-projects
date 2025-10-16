# 🖥️ EC2 Idle Instance Auto-Stop Lambda
 
A **serverless AWS automation** that identifies and stops idle EC2 instances using **CloudWatch Metrics**, **Lambda (Python)**, and **EventBridge scheduling** — reducing cloud costs while maintaining secure, least-privilege access.
 
---
 
## 🚀 Features
 
- Fetches CPU utilization metrics from **CloudWatch**
- Detects instances idle beyond a configurable duration
- Automatically stops idle EC2 instances using **boto3**
- Secured via a custom **IAM policy** with CloudWatch + EC2 permissions
- Handles metric delays with a “readiness check” before stopping
- Invoked periodically via **EventBridge rule (every 10 minutes)**
 
---
 
## 🧠 AWS Services Used
 
| Service | Purpose |
|----------|----------|
| **AWS Lambda (Python)** | Serverless execution logic |
| **CloudWatch Metrics** | CPUUtilization monitoring |
| **EventBridge** | Scheduled Lambda invocation |
| **IAM** | Role-based access and least privilege |
| **EC2** | Target instances for monitoring & stop |

![Architecture Diagram](screenshots/architecture-diagram.png) 
---
 
## 📂 Project Files
 
| File | Description |
|------|--------------|
| `lambda_function.py` | Main Lambda handler to fetch metrics and stop idle EC2s |
| `iam_policy.json` | IAM policy granting CloudWatch + EC2 permissions |
| `eventbridge_schedule.json` | Sample rule definition for periodic scheduling |
| `/screenshots` | Visual proof (Lambda config, CloudWatch metrics, logs, etc.) |
 
---

## 💰 Cost Optimization Impact
 
| 🧩 Metric | 💸 Before Automation | ⚙️ After Automation | 📉 Savings |
|:-----------|:--------------------|:--------------------|:------------|
| EC2 Instance Monthly Cost | **≈ $40 / month** | **≈ $8 – $20 / month** | ✅ **50 – 80 % reduction** |
| Annual Cost (Est.) | **≈ $480 / year** | **≈ $96 – $240 / year** | 💵 **Up to $384 saved annually** |
| Lambda + Monitoring Cost | Negligible (< $0.10 / month) | – | – |
 
**🔹 Result:**  
By implementing an AWS Lambda function with **EventBridge** and **CloudWatch** to automatically stop idle EC2 instances,  
the overall infrastructure cost was reduced by **50–80 %** without affecting availability.
 
💡 **50% cost reduction** for idle compute — scalable for multi-instance environments.

## 🧩 IAM Policy (Sample)
 
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowCloudWatchMetricsRead",
      "Effect": "Allow",
      "Action": [
        "cloudwatch:GetMetricStatistics",
        "cloudwatch:ListMetrics",
        "cloudwatch:GetMetricData",
        "ec2:DescribeInstances",
        "ec2:StopInstances"
      ],
      "Resource": "*"
    }
  ]
}
 
