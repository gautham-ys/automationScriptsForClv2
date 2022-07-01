'''add rule to eventbridge for each task-def per account in list'''
import boto3
import sys
import botocore.errorfactory
#import addTarget
import logging

def addTarget(account_id):
    '''add target to existing rule in eventbridge'''
    #
    #   prod subnets:   subnet-0961890eb6e230b76
    #                    
    #   security groups:  sg-04f0cdaa03c7a56e6 (shash01)     
    #

    try:
        client = boto3.client('events')
        response = client.put_targets(
            Rule=f'clv2_{account_id}',
            EventBusName='default',
            Targets=[{
                'Arn': f'arn:aws:ecs:us-east-1:612488371952:cluster/clv2test',
                'Id': account_id,
                'RoleArn': 'arn:aws:iam::612488371952:role/ECS-runallTasks-Clv2testcluster', 
                'EcsParameters': {
                    'TaskDefinitionArn': f'arn:aws:ecs:us-east-1:612488371952:task-definition/clv2_{account_id}',
                    'TaskCount': 1,
                    'LaunchType': 'FARGATE',
                    'NetworkConfiguration': {
                        'awsvpcConfiguration': {
                            'Subnets': [
                                'subnet-0961890eb6e230b76',
                            ],
                            'SecurityGroups': [
                                'sg-04f0cdaa03c7a56e6',
                            ],
                            'AssignPublicIp': 'DISABLED'
                        }
                    }
                },
            }]
        )
        return response
    except botocore.errorfactory.ClientError as e:
        print(e)
        sys.exit(1)

def addRule(account_id):
    '''add rule to eventbridge for each task-def per account in list'''
    # logger = logging.getLogger()
    # logger.setLevel(logging.INFO)
    # logger.addHandler(logging.StreamHandler(stream=sys.stdout))
    # logger.info(f'Adding rule for account {account_id}')
    print((f'Adding rule for account {account_id}'))

    client = boto3.client('events')
    response = client.put_rule(
        Name=f'clv2_{account_id}',
        ScheduleExpression='cron(30 12 * * ? *)',
        State='ENABLED',
        Description=f'clv2 - cost leakages for account id {account_id}',
        RoleArn='arn:aws:iam::612488371952:role/ECS-runallTasks-Clv2testcluster'
    )
    addTarget(account_id)
    #return response

def main():
    '''main function'''
    for account_id in sys.stdin.read().splitlines():
        addRule(account_id)
    
if __name__ == '__main__':
    main()