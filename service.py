# This Lambda function performs a dlx auth merge. 
# Event parameters: gaining_id (int), losing_id (int), user (str)
# Invocation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.invoke
# 
# <boto3 client>.invoke(
#   FunctionName='dlx-auth-merge', 
#   Payload=b'{"gaining_id": 1, "losing_id": 2, "user": "username"}'
# )

from unittest.mock import NonCallableMagicMock
from boto3 import client
from dlx.scripts import auth_merge

def handler(event, context):
    ssm = client('ssm', region_name='us-east-1')

    # dev db for now
    #connection_string = ssm.get_parameter(Name='connect-string')['Parameter']['Value']
    connection_string = ssm.get_parameter(Name='dev-dlx-connect-string')['Parameter']['Value']

    if connection_string is None:
        raise Exception('Unable to find DB connection credentials in AWS SSM')

    auth_merge.run(
        connect=connection_string,
        gaining_id=event.gaining_id,
        losing_id=event.losing_id,
        user=event.user,
        skip_prompt=True
    )
