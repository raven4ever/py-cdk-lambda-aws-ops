import logging
from datetime import time

from databases import DatabaseHandler
from ec2 import Ec2Handler
from ecs import EcsHandler
from utils import is_now_between


def selective_local_testing(looking_for):
    """
        Function to test the resource handler objects.
        The 600s waiting time is due to the long time RDS & DocDB clusters take to stop.
        This invocation will affect a limited set of resources.
    """

    test_databases(looking_for, 'stop')
    test_ec2s(looking_for, 'stop')
    test_ecs(looking_for, 'stop')

    logging.warning('Wait 10 mins for everything to stop')
    time.sleep(600)

    test_databases(looking_for, 'start')
    test_ec2s(looking_for, 'start')
    test_ecs(looking_for, 'start')


def test_databases(looking_for, operation):
    if is_now_between(time(8, 0), time(17, 0)):
        logging.error('Testing is allowed after business hours.')
    else:
        rds = DatabaseHandler(looking_for)

        instance_ids = rds.get_affected_cluster_ids()
        print(instance_ids)

        if operation == 'stop':
            logging.info('Stopping UFO RDS & DocDB clusters')
            rds.stop_rds_docd_clusters(['staging-rmn-imobillare-ufo', 'staging-rmn-imobillare-imobiliare'])
        elif operation == 'start':
            logging.info('Start UFO RDS & DocDB clusters')
            rds.start_rds_docd_clusters(['staging-rmn-imobillare-ufo', 'staging-rmn-imobillare-imobiliare'])
        else:
            logging.warning('Not a valid operation!!!')


def test_ec2s(looking_for, operation):
    if is_now_between(time(8, 0), time(17, 0)):
        logging.error('Testing is allowed after business hours.')
    else:
        ec2 = Ec2Handler(looking_for)

        instances = ec2.get_affected_instance_ids()
        print(instances)

        if operation == 'stop':
            logging.info('Stopping test EC2')
            ec2.stop_ec2_instances(['i-0bc48e401a650ccf9'])
        elif operation == 'start':
            logging.info('Start test EC2')
            ec2.start_ec2_instances(['i-0bc48e401a650ccf9'])
        else:
            logging.warning('Not a valid operation!!!')


def test_ecs(looking_for, operation):
    if is_now_between(time(8, 0), time(17, 0)):
        logging.error('Testing is allowed after business hours.')
    else:
        ecs = EcsHandler(looking_for)

        if operation == 'stop':
            logging.info('Stopping currently active ECS services')
            ecs.stop_ecs_services()
        elif operation == 'start':
            logging.info('Starting the ECS services')
            ecs.start_ecs_services()
        else:
            logging.warning('Not a valid operation!!!')
