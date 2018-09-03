import boto3

endpoint_url_ec2 = 'http://127.0.0.1:5000'
endpoint_url_asg = 'http://127.0.0.1:5002'
region_name = 'us-east-1'
zone = 'us-east-1a'

#ec2 client
ec2 = boto3.client('ec2', endpoint_url=endpoint_url_ec2, region_name=region_name)

#Launch instances
instance = ec2.run_instances(
     ImageId='ami-12345',
     MinCount=4,
     MaxCount=5
 )

instance_ids=[]
#List instances
for instances in instance['Instances']:
    instance_ids.append(instances["InstanceId"])
print("Instance ids: ")
print(instance_ids)

#Autoscaling client
autoscaling = boto3.client('autoscaling', endpoint_url=endpoint_url_asg, region_name=region_name)

#Create autoscaling configuration
config = autoscaling.create_launch_configuration(
    LaunchConfigurationName='my-launch-config'
)

#Create autoscaling group
asg = autoscaling.create_auto_scaling_group(
    AutoScalingGroupName='first_group',
    LaunchConfigurationName='my-launch-config',
    MinSize=5,
    MaxSize=10,
    AvailabilityZones=[zone]
)

#List autoscaling group details
asg_desc = autoscaling.describe_auto_scaling_groups(AutoScalingGroupNames=['first_group'])

for asg_name in asg_desc["AutoScalingGroups"]:
    name = asg_name["AutoScalingGroupName"]

print("ASG name")
print(name)

asg_instance_ids = []

#List autoscaling group instance ids
for instances in asg_desc["AutoScalingGroups"]:
    for instance in instances["Instances"]:
        asg_instance_ids.append(instance["InstanceId"])

print("ASG instance ids:")
print(asg_instance_ids)


