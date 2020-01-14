"""Manage AWS instance tags for telegraf."""

import boto.ec2

import requests

from . import agent
from . import message


def get_instance_id():
    """Retrieve instance ID."""
    response = requests.get("http://instance-data/latest/meta-data/instance-id")
    return response.content


def is_ec2_instance():
    """Validate EC2 instance."""
    try:
        response = requests.get("http://instance-data/latest/meta-data/instance-id")
    except requests.exceptions.RequestException:
        return False
    else:
        return bool(response.status_code == 200)


def tag_telegraf_config(aws_region, aws_key_id, aws_secret_key):
    """Configure telegraf for EC2 tags."""
    message.print_bold("Starting Telegraf Configuration for EC2 Tags")
    tags = get_instance_tags(aws_key_id, aws_secret_key, aws_region)

    return agent.tag_telegraf_config("ec2 metadata", tags)


def get_instance_tags(aws_access_key_id, aws_secret_key, aws_region):
    """Retrieve Ec2 tags from AWS."""
    conn = boto.ec2.connect_to_region(aws_region,
                                      aws_access_key_id=aws_access_key_id,
                                      aws_secret_access_key=aws_secret_key)

    if not is_ec2_instance():
        message.print_warn("This is not an EC2 instance.")
        return None

    try:
        reservations = conn.get_all_instances(instance_ids=[get_instance_id()])
    # pylint: disable=W0703
    except Exception:
        message.print_warn("Unable to authenticate with Amazon EC2 metadata"
                           " API for instance:" + get_instance_id())
        return None
    # Find the Instance object inside the reservation
    instance = reservations[0].instances[0]
    region = str(instance.region).replace('RegionInfo:', '')
    vpc_id = instance.vpc_id
    image_id = instance.image_id

    tags = instance.tags
    tags['aws-region'] = region
    tags['vpc-id'] = vpc_id
    tags['image-id'] = image_id
    return tags
