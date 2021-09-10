import boto3
import logging


class EcsHandler:
    """
        Class to handle the operations for ECS/Fargate services.
    """

    def __init__(self, looking_for_tags):
        """
            Constructor which will initialize the ECS Boto client.
        """
        self.looking_for_tags = looking_for_tags
        self.ecs = boto3.client('ecs')
        self.ssm = boto3.client('ssm')

    def get_all_services(self):
        logging.debug('[ECS] Retrieving cluster services...')
        svcs = self.ecs.describe_services(cluster=self.looking_for_tags['ECSClusterName'],
                                          services=self.looking_for_tags['ECSServices'])
        return svcs['services']

    def save_current_svc_state(self, cluster_name, svc_name, no_tasks):
        logging.debug(f'[ECS] Saving /ecs/{cluster_name}/{svc_name}/desired_count/{no_tasks}')
        self.ssm.put_parameter(Name=f'/ecs/{cluster_name}/{svc_name}/desired_count',
                               Value=str(no_tasks),
                               Type='String',
                               Overwrite=True)

    def get_saved_svc_state(self, cluster_name, svc_name):
        logging.debug(f'[ECS] Retrieving /ecs/{cluster_name}/{svc_name}/desired_count/')
        response = self.ssm.get_parameter(Name=f'/ecs/{cluster_name}/{svc_name}/desired_count')
        return response['Parameter']['Value']

    def start_ecs_services(self):
        for svc in self.get_all_services():
            logging.info(f"[ECS] Starting service {svc['serviceName']}")
            no_tasks = self.get_saved_svc_state(cluster_name=self.looking_for_tags['ECSClusterName'],
                                                svc_name=svc['serviceName'])
            self.update_service_count(cluster_name=self.looking_for_tags['ECSClusterName'],
                                      service_name=svc['serviceName'],
                                      count=int(no_tasks))

    def stop_ecs_services(self):
        for svc in self.get_all_services():
            logging.info(f"[ECS] Stopping service {svc['serviceName']}")
            self.save_current_svc_state(cluster_name=self.looking_for_tags['ECSClusterName'],
                                        svc_name=svc['serviceName'],
                                        no_tasks=svc['desiredCount'])
            self.update_service_count(cluster_name=self.looking_for_tags['ECSClusterName'],
                                      service_name=svc['serviceName'],
                                      count=0)

    def update_service_count(self, cluster_name, service_name, count):
        logging.debug(f'[ECS] Updating service {cluster_name}/{service_name} with {count}')
        self.ecs.update_service(cluster=cluster_name,
                                service=service_name,
                                desiredCount=count)
