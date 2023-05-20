import boto3

def stop_ec2_instances_by_tags(tag_key, tag_value):
    # Create an EC2 client
    ec2 = boto3.client('ec2')

    # Get all EC2 instances with the specified tag
    response = ec2.describe_instances(Filters=[
        {'Name': 'tag:{}'.format(tag_key), 'Values': [tag_value]}
    ])

    # Extract the instance IDs
    instance_ids = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])

    # Stop the instances
    if len(instance_ids) > 0:
        ec2.stop_instances(InstanceIds=instance_ids)
        print('Instances stopped: {}'.format(instance_ids))
    else:
        print('No instances to stop.')

def lambda_handler(event, context):
    # Specify the tag key and value to identify the instances
    tag_key = 'AutoShutdown'
    tag_value = 'true'

    # Stop the EC2 instances based on the tags
    stop_ec2_instances_by_tags(tag_key, tag_value)