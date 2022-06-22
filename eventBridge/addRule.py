'''add rule to eventbridge for each task-def per account in list'''
import boto3
import sys
import addTarget
import logging

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
    return addTarget.addTarget(account_id)
    #return response

def main():
    '''main function'''
    for account_id in sys.stdin.read().splitlines():
        addRule(account_id)
    
if __name__ == '__main__':
    main()