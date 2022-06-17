'''
1. create log for each account id
2. create task definition for each account id
3. create rule for each account id
4. add target to each rule

'''

import sys
import logging
import botocore.errorfactory

import logGroup.createLogGroup as createLogGroup
import taskDef.CreateTaskDefinition as CreateTaskDefinition
import eventBridge.addRule as addRule
import eventBridge.addTarget as addTarget

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))

def main():
    '''main function'''
    try:
        for account_id in sys.stdin.read().splitlines():
            createLogGroup.createLogGroup(account_id)
            CreateTaskDefinition.create_clv2_task_definition(account_id)
            addRule.addRule(account_id)
            addTarget.addTarget(account_id)

    except botocore.errorfactory.ClientError as e:
        logger.error(str(e))
        sys.exit(1)
    
if __name__ == '__main__':
    main()