#!/usr/bin/env python3

from aws_cdk import core

from infra.lambda_infra import AwsOpsStack

app = core.App()
AwsOpsStack(app, "AwsOpsStack")

app.synth()
