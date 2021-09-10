import logging
import time

from databases import DatabaseHandler
from ec2 import Ec2Handler
from ecs import EcsHandler
from utils import is_substring_in_string

# The only required setup you need to do
looking_for = {
    'TagName': 'Environment',
    'TagValue': 'staging',
    'ECSClusterName': 'staging-main',
    'ECSServices': [
        'svc1-staging',
        'sv2-staging'
    ]
}

####################################
# DO NOT MODIFY BEYOND THIS POINT! #
####################################
# logger setup
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
# AWS resources handlers
rds = DatabaseHandler(looking_for)
ec2 = Ec2Handler(looking_for)
ecs = EcsHandler(looking_for)


def lambda_handler(event, context):
    """
        This is the Lambda handler function. The code will be executed when an event is generated.
    """
    operation_type = event['operation']

    if operation_type == 'start':
        logging.info('Starting everything...')
        rds.start_rds_docd_clusters()
        ec2.start_ec2_instances()
        ecs.start_ecs_services()
        return_msg = f'Successfully started the resources...'
    elif operation_type == 'stop':
        logging.info('Stopping everything...')
        ecs.stop_ecs_services()
        ec2.stop_ec2_instances()
        rds.stop_rds_docd_clusters()
        return_msg = f'Successfully stopped the resources...'
    else:
        return_msg = f'Operation {operation_type} cannot be handled!'

    return return_msg


def full_local_testing():
    """
        Function to mimic calls to the Lambda handler.
        The function will verify the content of each of the 3 possible responses.
        The 600s waiting time is due to the long time RDS & DocDB clusters take to stop.
        This invocation will affect ALL the resources.
    """
    responses = {}

    # Test a stop event
    event = {
        'operation': 'stop'
    }
    responses['stop'] = lambda_handler(event, None)

    logging.warning('Wait 10 mins for everything to stop')
    time.sleep(600)

    # Test a start event
    event = {
        'operation': 'start'
    }
    responses['start'] = lambda_handler(event, None)

    logging.warning('Wait 10 sec for everything to settle')
    time.sleep(10)

    # Test an invalid event
    event = {
        'operation': 'invalid'
    }
    responses['invalid'] = lambda_handler(event, None)

    # Verify the output content
    assert is_substring_in_string('stopped', responses['stop'])
    assert is_substring_in_string('started', responses['start'])
    assert is_substring_in_string('invalid', responses['invalid'])
    logging.info(f'The testing responses are {responses}')


if __name__ == '__main__':
    """
        This code will NOT run in the context of the Lambda function !!!
        It's for local testing purposes only !!!
    """

    # either run the selective testing
    # selective_local_testing(looking_for)

    # or the full lambda code
    full_local_testing()
