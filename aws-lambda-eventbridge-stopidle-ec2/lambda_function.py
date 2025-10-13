import boto3, datetime, os
 
ec2 = boto3.client('ec2')
cloudwatch = boto3.client('cloudwatch')

# ==== CONFIGURATION ====
INSTANCE_NAME = 'my-app-instance-1'
CPU_THRESHOLD = 1.0               # percent
NETWORK_THRESHOLD = 1000000       # bytes (≈1 MB)
IDLE_PERIOD_MINUTES = 30          # how long to look back
# ========================
 
def lambda_handler(event, context):
    try:
        INSTANCE_ID = get_instance_id_by_name(INSTANCE_NAME)
        print(f"Found instance ID: {INSTANCE_ID} for name: {INSTANCE_NAME}")
    except Exception as e:
        print(f"Error: {e}")
        return
    end_time = datetime.datetime.utcnow()
    start_time = end_time - datetime.timedelta(minutes=IDLE_PERIOD_MINUTES)
 
    # --- Fetch CPUUtilization ---
    cpu_metrics = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'InstanceId', 'Value': INSTANCE_ID}],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average']
    )
 
    # --- Fetch NetworkIn ---
    net_metrics = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='NetworkIn',
        Dimensions=[{'Name': 'InstanceId', 'Value': INSTANCE_ID}],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average']
    )
 
    if not cpu_metrics['Datapoints'] or not net_metrics['Datapoints']:
        print("No metrics available yet; skipping.")
        return
 
    avg_cpu = sum(dp['Average'] for dp in cpu_metrics['Datapoints']) / len(cpu_metrics['Datapoints'])
    avg_net = sum(dp['Average'] for dp in net_metrics['Datapoints']) / len(net_metrics['Datapoints'])
 
    print(f"Average CPU: {avg_cpu:.2f}%, NetworkIn: {avg_net:.2f} bytes")
 
    if avg_cpu < CPU_THRESHOLD and avg_net < NETWORK_THRESHOLD:
        print(f"Instance {INSTANCE_ID} seems idle. Attempting to stop it.")
        ec2.stop_instances(InstanceIds=[INSTANCE_ID])
    else:
        print(f"Instance {INSTANCE_ID} still active; skipping stop.")
 

 def get_instance_id_by_name(instance_name):
    """Get instance ID from instance name tag"""
    response = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Name', 'Values': [instance_name]},
            {'Name': 'instance-state-name', 'Values': ['running', 'stopped']}
        ]
    )
    
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            return instance['InstanceId']
    
    raise Exception(f"Instance with name '{instance_name}' not found")
