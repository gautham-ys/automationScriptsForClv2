'''create a log group for each account id passed as an argument'''

import boto3
import sys
import botocore.errorfactory

def createLogGroup(account_id):
    '''create a log group for each account id passed as an argument'''
    try:
        client = boto3.client('logs')
        response = client.create_log_group(
            logGroupName=f'/ecs/clv2withLogging/{account_id}'
        )
        return response
    except botocore.errorfactory.ClientError:
        print(f'log group already exists for {account_id}')
        return {'logGroupName': f'/ecs/clv2/{account_id}'}

def __main__():
    for id in sys.stdin.read().splitlines():
        response = createLogGroup(id)
        print(response)

if __name__ == '__main__':
    __main__()