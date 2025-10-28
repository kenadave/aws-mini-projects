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

## 💰 AWS Cost Comparison (Before vs After Automation)
 
| 🧩 Service | 💸 Before Automation (Monthly) | ⚙️ After Automation (Monthly) | 📉 Savings |
|:------------|:-------------------------------|:-------------------------------|:------------|
| **EC2 Instance (Compute)** | $35.00 | $7.00 – $17.00 | ✅ 50–80% |
| **EBS Storage (Root Volume)** | $3.00 | $3.00 | ⚙️ No change |
| **Data Transfer / Networking** | $1.50 | $0.50 | 🔻 Reduced usage |
| **CloudWatch Monitoring** | $0.30 | $0.30 | ⚙️ No change |
| **Lambda (Automation Function)** | – | $0.05 | 🪶 Negligible |
| **EventBridge Scheduler** | – | $0.01 | 🪶 Negligible |
| **Total (Approx.)** | **$40 / month** | **$8.86 – $20.36 / month** | **💵 50–80% savings** |
 
✅ **Result:**  
By using a Lambda + EventBridge setup to automatically stop idle EC2 instances, total monthly cost reduced from **≈ $40 → $9–20**,  
saving up to **$31/month (~$370/year)** without affecting performance.

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



## 💰 AWS Cost Comparison
 
| Service | Before Automation (Monthly) | After Automation (Monthly) | Quarterly (Before) | Quarterly (After) |
|:--------|:----------------------------:|:---------------------------:|:------------------:|:-----------------:|
| **EC2 (Compute)** | $35.00 | $7.00 – $17.00 | $105.00 | $21.00 – $51.00 |
| **EBS (Storage)** | $3.00 | $3.00 | $9.00 | $9.00 |
| **Data Transfer** | $1.50 | $0.50 | $4.50 | $1.50 |
| **CloudWatch** | $0.30 | $0.30 | $0.90 | $0.90 |
| **Lambda (Automation)** | – | $0.003 | – | $0.009 |
| **EventBridge (Scheduler)** | – | $0.004 | – | $0.012 |
| **🧾 Total (Approx.)** | **$40.00 / month** | **$8.29 – $20.80 / month** | **$120.00 / quarter** | **$24.87 – $62.40 / quarter** |
 
✅ **Overall Savings:** ~50 – 80 % reduction in EC2 costs through automated idle-stop using AWS Lambda + EventBridge.

