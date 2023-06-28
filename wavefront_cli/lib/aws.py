"""Manage AWS instance tags for telegraf."""

import boto3

import requests

from . import agent
from . import message


REQUEST_TIMEOUT = 10


def get_instance_id():
    """Retrieve instance ID."""
    response = requests.get(
        "http://instance-data/latest/meta-data/instance-id",
        timeout=REQUEST_TIMEOUT)
    return response.content


def is_ec2_instance():
    """Validate EC2 instance."""
    try:
        response = requests.get(
            "http://instance-data/latest/meta-data/instance-id",
            timeout=REQUEST_TIMEOUT)
    except requests.exceptions.RequestException:
        return False
    return bool(response.status_code == 200)


def tag_telegraf_config(aws_region, aws_key_id, aws_secret_key):
    """Configure telegraf for EC2 tags."""
    message.print_bold("Starting Telegraf Configuration for EC2 Tags")
    tags = get_instance_tags(aws_key_id, aws_secret_key, aws_region)

    return agent.tag_telegraf_config("ec2 metadata", tags)


def get_instance_tags(aws_access_key_id, aws_secret_key, aws_region):
    """Retrieve Ec2 tags from AWS."""
    conn = boto3.session.Session().client('ec2', region_name=aws_region,
                                          aws_access_key_id=aws_access_key_id,
                                          aws_secret_access_key=aws_secret_key)

    if not is_ec2_instance():
        message.print_warn("This is not an EC2 instance.")
        return None

    try:
        reservations = conn.describe_instances(InstanceIds=[get_instance_id()])
    except boto3.exceptions.botocore.exceptions.ClientError:
        message.print_warn("Unable to authenticate with Amazon EC2 metadata"
                           " API for instance:" + get_instance_id())
        return None
    # Find the Instance object inside the reservation
    instance = reservations['Reservations'][0]['Instances'][0]

    tags = {t['Key']: t['Value'] for t in instance['Tags']}
    tags['aws-region'] = aws_region
    tags['vpc-id'] = instance['VpcId']
    tags['image-id'] = instance['ImageId']
    return tags
