'''Creates a task definition to run clv2 driver code on the ECS cluster for a given account id passed as an argument'''

import boto3
import json
import sys

template_task_def_str = open('template_task_def.json', 'r').read()

template_task_def = json.loads(template_task_def_str)
print(template_task_def)

def create_clv2_task_definition(account_id, memory='512', cpu='512'):
    '''Creates a task definition to run clv2 driver code on the ECS cluster for a given account id passed as an argument'''

    # set the account id in the log group and container name and command
    container_name = f'clv2_{account_id}'
    aws_logs_group = f'/ecs/clv2withLogging/{account_id}'
    template_task_def['containerDefinitions'][0]['command'][0] = account_id
    template_task_def['containerDefinitions'][0]['name'] = container_name
    template_task_def['containerDefinitions'][0]['logConfiguration']['options']['awslogs-group'] = aws_logs_group

    # custom memory
    template_task_def['containerDefinitions'][0]['memory'] = memory

    # main
    client = boto3.client('ecs')
    response = client.register_task_definition(
        family='clv2_' + account_id,
        taskRoleArn=template_task_def['taskRoleArn'],
        executionRoleArn=template_task_def['executionRoleArn'],
        networkMode='awsvpc',
        containerDefinitions=template_task_def['containerDefinitions'],
        placementConstraints=template_task_def['placementConstraints'],
        requiresCompatibilities=['FARGATE'],
        runtimePlatform=template_task_def['runtimePlatform'],
        cpu='256',
        memory='512'
    )
    return response

def main():
    account_ids = [id for id in sys.stdin.read().splitlines()]
    for account_id in account_ids:
        response = create_clv2_task_definition(account_id)
        print(response)
    return 0

if __name__ == '__main__':
    main()
    