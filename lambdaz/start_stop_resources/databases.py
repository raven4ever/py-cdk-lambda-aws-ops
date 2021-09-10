import boto3
import logging
from botocore.exceptions import ClientError


class DatabaseHandler:
    """
        Class to handle the operations for RDS and DocDB clusters.
        Due to AWS bugs (https://github.com/aws/aws-cli/issues/6300) a single client is needed for both types.
    """

    def __init__(self, looking_for_tags: dict):
        """
            Constructor which will initialize the RDS & DocDB Boto client.
        """
        self.looking_for_tags = looking_for_tags
        self.rds = boto3.client('rds')

    def get_affected_cluster_ids(self):
        logging.debug('[DB] Retrieving affected instances...')

        affected_cluster_ids = list()

        all_clusters = self.rds.describe_db_clusters()

        for cluster in all_clusters['DBClusters']:
            if self.is_cluster_matching_tags(cluster):
                affected_cluster_ids.append(cluster['DBClusterIdentifier'])

        return affected_cluster_ids

    def is_cluster_matching_tags(self, cluster):
        logging.debug(f'[DB] Verifying tags for {cluster}...')
        if 'TagList' in cluster:
            cluster_tags = cluster['TagList']
        else:
            cluster_arn = cluster['DBClusterArn']
            cluster_tags = self.rds.list_tags_for_resource(ResourceName=cluster_arn)['TagList']

        for tag in cluster_tags:
            if tag['Key'] == self.looking_for_tags['TagName'] and tag['Value'] == self.looking_for_tags['TagValue']:
                return True
        return False

    def start_rds_docd_clusters(self, ids=None):
        clusters_ids = ids or self.get_affected_cluster_ids()
        for cluster in clusters_ids:
            logging.info(f'[DB] Trying to start cluster {cluster}')
            try:
                self.rds.start_db_cluster(DBClusterIdentifier=cluster)
            except ClientError as err:
                if err.response['Error']['Code'] == 'InvalidDBClusterStateFault':
                    logging.warning(f'[DB] Cluster {cluster} is already started!!!')
                else:
                    print(f'[DB] Unexpected error: {err}')

    def stop_rds_docd_clusters(self, ids=None):
        clusters_ids = ids or self.get_affected_cluster_ids()
        for cluster in clusters_ids:
            logging.info(f'[DB] Trying to stop cluster {cluster}')
            try:
                self.rds.stop_db_cluster(DBClusterIdentifier=cluster)
            except ClientError as err:
                if err.response['Error']['Code'] == 'InvalidDBClusterStateFault':
                    logging.warning(f'[DB] Cluster {cluster} is already stopped!!!')
                else:
                    print(f'Unexpected error: {err}')
