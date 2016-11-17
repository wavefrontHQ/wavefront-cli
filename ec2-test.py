import boto.ec2
conn=boto.ec2.connect_to_region("us-west-2",aws_access_key_id='AKIAJTNM56KXAMQOCZNA',aws_secret_access_key='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')
# Find a specific instance, returns a list of Reservation objects
reservations = conn.get_all_instances(instance_ids=['i-0465f590'])
# Find the Instance object inside the reservation
instance = reservations[0].instances[0]
print(instance.tags)

