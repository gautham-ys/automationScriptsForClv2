'''add target to existing rule in eventbridge'''

import boto3
import botocore.errorfactory
import logging
import sys

def addTarget(account_id):
    '''add target to existing rule in eventbridge'''
    #
    #   prod subnets:   subnet-0961890eb6e230b76
    #                    
    #   security groups:  sg-04f0cdaa03c7a56e6 (shash01)     
    #

    logger = logging.getLogger()
    try:
        client = boto3.client('events')
        response = client.put_targets(
            Rule=f'clv2_{account_id}',
            Targets=[{
                'Arn': f'arn:aws:ecs:us-east-1:612488371952:cluster/clv2test',
                'Id': account_id,
                'RoleArn': 'arn:aws:iam::612488371952:role/ECS-runallTasks-Clv2testcluster',
                'EcsParameters': {
                    'TaskDefinitionArn': f'arn:aws:ecs:us-east-1:612488371952:task-definition/clv2_{account_id}',
                    'TaskCount': 1,
                    'LaunchType': 'FARGATE',
                    'EnableECSManagedTags': True
                    'NetworkConfiguration': {
                        'awsvpcConfiguration': {
                            'Subnets': [    # prod subnets
                                'subnet-0961890eb6e230b76',
                            ],
                            'SecurityGroups': [
                                'sg-04f0cdaa03c7a56e6', #shash01
                            ],
                            'AssignPublicIp': 'DISABLED'
                        }
                    }
                }
            }]
        )
        return response

    except botocore.errorfactory.ClientError as e:
        logger.error(str(e))
        sys.exit(1)

