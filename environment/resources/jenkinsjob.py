import boto3
import json

with open('./environment/deploy.json') as data_file:
    config = json.load(data_file)

for region in config:
    print region
    client = boto3.client('cloudformation', region_name=region)
    if config[region]['enabled']:
        print "    region %s is enabled" % region
        with open('./environment/app.json', 'r') as cfnTemplate:
            templateBody=cfnTemplate.read()
        try:
            client.describe_stacks(StackName='app')
        except:
            print '    deploying app stack'
            response = client.create_stack(
                StackName='app',
                TemplateBody=templateBody,
                Capabilities=[
                    'CAPABILITY_IAM',
                ],
                OnFailure='ROLLBACK',
            )
        else:
            print '    updating app stack'
            try:
                response = client.update_stack(
                    StackName='app',
                    TemplateBody=templateBody,
                    Capabilities=[
                        'CAPABILITY_IAM',
                    ]
                )
            except:
                print '    No updates are to be performed'
    else:
        print "    region %s is disabled, ensuring app stack does not exist" % region
        try:
            client.describe_stacks(StackName='app')
        except:
            print "    app stack does not exist in region %s, continuing" % region
            continue
        else:
            print "    app stack found in region %s, deleting" % region
            client.delete_stack(StackName='app')


#to access jenkins env vars in Python:
#import os
#workspace = os.environ['WORKSPACE']
