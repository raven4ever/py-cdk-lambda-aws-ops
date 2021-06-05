import time

import boto3

ec2 = boto3.resource('ec2')


def get_affected_instance_ids():
    affected_instances = ec2.instances.filter(Filters=[
        {'Name': 'tag:OnlyByDay', 'Values': ['true']}
    ])
    ids = [inst.id for inst in affected_instances]
    return ids


def stop_instances(ids):
    print(f'Stopping instances with the ids: {ids}')
    ec2.instances.filter(InstanceIds=ids).stop()


def start_instances(ids):
    print(f'Starting instances with the ids: {ids}')
    ec2.instances.filter(InstanceIds=ids).start()


def lambda_handler(event, context):
    operation_type = event['operation']

    instance_ids = get_affected_instance_ids()

    if operation_type == 'start':
        start_instances(instance_ids)
        return_msg = f'Started instances with ids: {instance_ids}...'
    elif operation_type == 'stop':
        stop_instances(instance_ids)
        return_msg = f'Stropped instances with ids: {instance_ids}...'
    else:
        return_msg = f'Operation {operation_type} cannot be handled!'

    return return_msg


if __name__ == '__main__':
    instance_ids = get_affected_instance_ids()

    stop_instances(instance_ids)

    time.sleep(20)

    start_instances(instance_ids)
