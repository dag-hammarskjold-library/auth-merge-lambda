# This Lambda function performs a dlx auth merge. 
# Event parameters: gaining_id (int), losing_id (int)
# invocation: `<boto3 client>.invoke(FunctionName='dlx-auth-merge', payload='{"gaining_id": 1, "losing_id: 2"}')`

from time import time
from boto3 import client as botoclient
from dlx import DB
from dlx.marc import Auth

def handler(event, context):
    ssm = botoclient('ssm', region_name='us-east-1')

    try:
        # dev db for now
        #connection_string = ssm.get_parameter(Name='connect-string')['Parameter']['Value']
        connection_string = ssm.get_parameter(Name='dev-dlx-connect-string')['Parameter']['Value']
    except:
        raise Exception('Unable to get AWS SSM parameter')

    DB.connect(connection_string)
    print(f'Merging auth {event.losing_id} into {event.gaining_id}')
    started = time()
    gaining_auth = Auth.from_id(event.gaining_id)
    
    if gaining_auth is None:
        raise Exception(f'Gaining record {event.gaining_id} not found')

    losing_auth = Auth.from_id(event.losing_id)

    if losing_auth is None:
        raise Exception(f'Losing record {event.losing_id} not found')

    print(f'{losing_auth.in_use(usage_type="bib")} bibs and {losing_auth.in_use(usage_type="auth")} auths will be updated')

    # perform merge
    gaining_auth.merge(losing_auth)
    print(f'Finished in {started - time()} seconds')
