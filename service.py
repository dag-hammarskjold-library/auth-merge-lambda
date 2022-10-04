# This Lambda function performs a dlx auth merge. 
# Event parameters: gaining_id (int), losing_id (int), user (str)
# Invocation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.invoke
# 
# boto3.client('lambda').invoke(
#   FunctionName='dlx-auth-merge', 
#   Payload=b'{"connect": <mongodb connection string>, gaining_id": 1, "losing_id": 2, "user": "username"}'
# )

from dlx.scripts import auth_merge

def handler(event, context):
    for _ in ['connect', 'gaining_id', 'losing_id', 'user']:
        if _ not in event.keys(): raise Exception('event dict missing one or more required keys: connect, gaining_id, losing_id, user')

    auth_merge.run(
        connect=event['connect'],
        gaining_id=event['gaining_id'],
        losing_id=event['losing_id'],
        user=event['user'],
        skip_prompt=True
    )
