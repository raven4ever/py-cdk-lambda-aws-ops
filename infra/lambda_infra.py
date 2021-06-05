from aws_cdk import (
    core,
    aws_lambda as lmdb,
)
from aws_cdk.aws_lambda_python import PythonFunction


class AwsOpsStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create function
        stop_start_ec2s_function = PythonFunction(self, 'Stop/Start EC2s',
                                                  function_name='stop_start_ec2s_function',
                                                  runtime=lmdb.Runtime.PYTHON_3_8,
                                                  index='main.py',
                                                  handler='lambda_handler',
                                                  entry='lambdaz/start_stop_ec2',
                                                  current_version_options=lmdb.VersionOptions(
                                                      removal_policy=core.RemovalPolicy.RETAIN)
                                                  )

        dev = lmdb.Alias(self, 'development', alias_name='development',
                         version=stop_start_ec2s_function.current_version)
