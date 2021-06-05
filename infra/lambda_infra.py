from aws_cdk import (
    core,
    aws_lambda as lmdb,
    aws_iam as iam
)
from aws_cdk.aws_lambda_python import PythonFunction


class AwsOpsStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stop_start_ec2s_role = iam.Role(self, 'StopStartEc2sLambdaRole',
                                        role_name='StopStartEc2sLambdaRole',
                                        assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'))
        stop_start_ec2_policy = iam.Policy(self, 'EC2StopStartAccessPolicy',
                                           policy_name='EC2StopStartAccessPolicy',
                                           statements=[
                                               iam.PolicyStatement(actions=['ec2:StartInstances',
                                                                            'ec2:DescribeTags',
                                                                            'ec2:StopInstances',
                                                                            'ec2:DescribeInstances'],
                                                                   resources=['*'])
                                           ])
        stop_start_ec2s_role.attach_inline_policy(stop_start_ec2_policy)

        stop_start_ec2s_function = PythonFunction(self, 'Stop/Start EC2s',
                                                  function_name='stop_start_ec2s_function',
                                                  runtime=lmdb.Runtime.PYTHON_3_8,
                                                  index='main.py',
                                                  handler='lambda_handler',
                                                  entry='lambdaz/start_stop_ec2',
                                                  role=stop_start_ec2s_role,
                                                  current_version_options=lmdb.VersionOptions(
                                                      removal_policy=core.RemovalPolicy.RETAIN)
                                                  )

        dev = lmdb.Alias(self, 'development', alias_name='development',
                         version=stop_start_ec2s_function.current_version)
