import requests
import subprocess
import json
import sys
import system
import agent
import boto.ec2
import message
import string

def get_instance_id():
    r = requests.get("http://instance-data/latest/meta-data/instance-id")
    return r.content

def is_ec2_instance():
    r = requests.get("http://instance-data/latest/meta-data/instance-id")
    if r.status_code == 200:
        return True
    else:
        return False

def tag_telegraf_config(aws_region, aws_key_id, aws_secret_key):

    message.print_bold("Starting Telegraf Configuration for EC2 Tags")
    tags = get_instance_tags(aws_key_id, aws_secret_key, aws_region)

    if not tags:
        return False

    tags_pre = "- Start EC2 Tags -"
    tags_post = "- End EC2 Tags- "
    tagStr = "  # %s\n" % (tags_pre)
    for k,v in tags.iteritems():
        tagStr += '\t%s = "%s"\n' % (k.lower(),v)
    tagStr += "  # %s\n" % (tags_post)
    try:
        tagTxt = open("tags.txt","w")
        tagTxt.write(tagStr)
        tagTxt.close()
    except:
        message.print_warn("Error writing tags.txt: " + sys.exc_info()[0])
        return False


    # remove existing ec2 tags
    conf = agent.conf_path
    cmd = "sudo sed -i '/%s/,/%s/d' %s" % (tags_pre, tags_post, conf)
    #print cmd
    output = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)

    cmd = "sudo sed -i '/\[global_tags\]/r tags.txt' %s" % (conf)
    try:
        output = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
    except:
        message.print_warn("Error overwriting telegraf.conf. Is the file located at " +  conf + "? " + sys.exc_info()[0])
        return False

    message.print_success("Finished Telegraf Configuration for EC2 Tags")
    return True

def get_instance_tags(aws_access_key_id, aws_secret_access_key, aws_region):
    conn = boto.ec2.connect_to_region(aws_region, aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key)
    reservations = conn.get_all_instances(instance_ids=[get_instance_id()])
    # Find the Instance object inside the reservation
    instance = reservations[0].instances[0]
    region = str(instance.region).replace('RegionInfo:','')
    vpc_id = instance.vpc_id
    image_id = instance.image_id

    tags = instance.tags
    tags['aws-region'] = region
    tags['vpc-id'] = vpc_id
    tags['image-id'] = image_id
    return tags



