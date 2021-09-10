# Lambda Stop & Start Unused Infrastructure

## Context

In the effort to reduce the overall AWS costs we decided to stop all the AWS infrastructure that is not needed to run
after business hours.

In the first phase, this process will stop all RDS, DocumentDB, EC2 and Fargate instances related to the staging
environment.

## How it works

The project uses the [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) library provided by
AWS.

## Structure

## Requirements

### Local

The development of the whole project was made locally as an independent Python project.

The main requirement is to have a Python 3.8+ environment set up with the `boto3` library installed.

```shell
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Lambda