import boto3
import logging

#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

TopicArn = 'Write the Topic ARN for notification here'

#define the connection
ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    # Use the filter() method of the instances collection to retrieve
    # all running EC2 instances.
    filters = [
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
    ]
    
    #filter the instances
    instances = ec2.instances.filter(Filters=filters)

    #locate Untagged untagged instances
    name_untaggedInstances = [instance.id for instance in instances if 'Name' not in [t['Key'] for t in instance.tags]]
    #The below line was added for debugging 
    print name_untaggedInstances
    #commenting out the unwanted tags from the list of all the logs    
    #ptower_untaggedInstances = [instance.id for instance in instances if 'Product Tower' not in [t['Key'] for t in instance.tags]]
    app_untaggedInstances = [instance.id for instance in instances if 'Application' not in [t['Key'] for t in instance.tags]]
    #cla_untaggedInstances = [instance.id for instance in instances if 'Clarity ID' not in [t['Key'] for t in instance.tags]]
    #spos_untaggedInstances = [instance.id for instance in instances if 'Security Posture' not in [t['Key'] for t in instance.tags]]
    #scon_untaggedInstances = [instance.id for instance in instances if 'Support Contact' not in [t['Key'] for t in instance.tags]]
    appown_untaggedInstances = [instance.id for instance in instances if 'Application Owner' not in [t['Key'] for t in instance.tags]]
    #dom_untaggedInstances = [instance.id for instance in instances if 'Domain' not in [t['Key'] for t in instance.tags]]
    #untaggedInstances = untaggedInstances + ptower_untaggedInstances + app_untaggedInstances + cla_untaggedInstances + spos_untaggedInstances + scon_untaggedInstances + appown_untaggedInstances + dom_untaggedInstances
    untaggedInstances = name_untaggedInstances + app_untaggedInstances + appown_untaggedInstances
    untaggedInstances = list(set(untaggedInstances))
    print untaggedInstances
    #print the instances for logging purposes
    #print untaggedInstances 
    
    #make sure there are actually instances to shut down. 
#    if len(untaggedInstances) > 0:
        #perform the shutdown
         #print "Right now doing testing"
#         shuttingDown = ec2.instances.filter(InstanceIds=untaggedInstances).stop()
#         publish_to_sns(shuttingDown)
#         print shuttingDown
    #     print untaggedInstances
#    else:
#        print "Nothing to see here"
    if len(ListRunningUnTaggedInstances) > 0:
            #perform the shutdown
        for instance in ListRunningUnTaggedInstances:
            s+=instance + "\n"
        print s
        stopInstance(ListRunningUnTaggedInstances)
        #publish_to_sns(s)    
    else:
        print "Nothing to see here..!"
        
def stopInstance(instanceId):
#    instanceId = ['TestingID']
    ec2.instances.filter(InstanceIds=instanceId).stop()


def publish_to_sns(message):
    sns = boto3.client('sns')
    sns_message = str(message)
    response = sns.publish(TopicArn=Topic_Arn,Subject = "Instance Shutdown Notification for account " + account, Message = sns_message)