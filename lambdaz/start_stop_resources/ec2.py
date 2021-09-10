import boto3
import logging


class Ec2Handler:
    """
       Class to handle the operations for EC2 machines.
    """

    def __init__(self, looking_for_tags: dict):
        """
            Constructor which will initialize the EC2 Boto client.
        """
        self.looking_for_tags = looking_for_tags
        self.ec2 = boto3.resource('ec2')

    def get_affected_instance_ids(self):
        logging.debug('[EC2] Retrieving affected EC2 instances...')
        affected_instances = self.ec2.instances.filter(Filters=[
            {
                'Name': f"tag:{self.looking_for_tags['TagName']}",
                'Values': [self.looking_for_tags['TagValue']]
            }
        ])
        instance_ids = [inst.id for inst in affected_instances]
        return instance_ids

    def stop_ec2_instances(self, ids=None):
        instance_ids = ids or self.get_affected_instance_ids()
        logging.info(f'[EC2] Stopping instances with the ids: {instance_ids}')
        self.ec2.instances.filter(InstanceIds=instance_ids).stop()

    def start_ec2_instances(self, ids=None):
        instance_ids = ids or self.get_affected_instance_ids()
        logging.info(f'[EC2] Starting instances with the ids: {instance_ids}')
        self.ec2.instances.filter(InstanceIds=instance_ids).start()
