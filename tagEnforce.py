import boto3
import logging

#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)
Topic_Arn = 'sns arn '
#define the connection
ec2 = boto3.resource('ec2')
account = "my acc"
#define filters
    # Use the filter() method of the instances collection to retrieve
    # all running EC2 instances.
TaggedRunningfilters = [{
            'Name': 'tag:Name',
            'Values': ['*']
        },
 #       {'Name': 'tag:ResourceName',
#        'Values': ['*']
#        },
#        {'Name': 'tag:ProductTower',
#        'Values': ['*']
#        },
        {'Name': 'tag:Application',
        'Values': ['*']
        },
#        {'Name': 'tag:ClarityID',
#        'Values': ['*']
#        },
#        {'Name': 'tag:SecurityPosture',
#        'Values': ['*']
#        },
#        {'Name': 'tag:SupportContact',
#        'Values': ['*']
#        },
        {'Name': 'tag:ApplicationOwner',
        'Values': ['*']
        },
#        {'Name': 'tag:Domain',
#        'Values': ['*']
#        },
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
    }
    ]
TaggedStoppedfilter=[{
           'Name': 'tag:Name',
            'Values': ['*']
        },
#        {'Name': 'tag:ResourceName',
#        'Values': ['*']
#        },
#        {'Name': 'tag:ProductTower',
#        'Values': ['*']
#        },
        {'Name': 'tag:Application',
        'Values': ['*']
        },
#        {'Name': 'tag:ClarityID',
#        'Values': ['*']
#        },
#        {'Name': 'tag:SecurityPosture',
#        'Values': ['*']
#        },
#        {'Name': 'tag:SupportContact',
#        'Values': ['*']
#        },
        {'Name': 'tag:ApplicationOwner',
        'Values': ['*']
        },
#        {'Name': 'tag:Domain',
#        'Values': ['*']
#        },
        {
            'Name': 'instance-state-name', 
           'Values': ['stopped']
    }
    ]
AllStopped=[{
            'Name': 'instance-state-name', 
            'Values': ['stopped']
    }]
AllRunning=[{
            'Name': 'instance-state-name', 
            'Values': ['running']
    }]
AllPending=[{
            'Name': 'instance-state-name', 
            'Values': ['pending']
    }]
AllTerminated=[{
            'Name': 'instance-state-name', 
            'Values': ['terminated']
    }]

def lambda_handler(event, context):

    s = ""
    #filter the instances
    RunningTInstances = ec2.instances.filter(Filters=TaggedRunningfilters) # all runnig tagged inst
    RunningInstances = ec2.instances.filter(Filters=AllRunning)  # all ruuning
    StoppedInstances = ec2.instances.filter(Filters=AllStopped) # All stoped
    StoppedTInstances = ec2.instances.filter(Filters=TaggedStoppedfilter) # all stopped tagged
    TerminatedInstances = ec2.instances.filter(Filters=AllTerminated) # all stopped tagged
    AllInstances= ec2.instances.all()  # all instances in acc
#   ----------------------------------------------------------------------------------------     

    ListAllRunningTInstances = [instance.id for instance in RunningTInstances]
    ListAllRunningInstances = [instance.id for instance in RunningInstances]
    ListAllStoppedInstances = [instance.id for instance in StoppedInstances]
    ListAllTerminatedInstances = [instance.id for instance in TerminatedInstances]
    ListAllStoppedTInstances = [instance.id for instance in StoppedTInstances]
    ListAllindtance = [instance.id for instance in AllInstances]
    ListRunningUnTaggedInstances = list(
        (
            (set(ListAllindtance) - set(ListAllRunningTInstances)
                ) - set(ListAllStoppedInstances)
            ) - set(ListAllTerminatedInstances)
        )
#---------------------------------------------------------------------------------------------
    print "Following is the instance summary for account %s" %account
    print "Total Instances = %d" %len(ListAllindtance)
    print "Running and tagged instances = %d" %len(ListAllRunningTInstances)
    print "Running and untagged instances= %d" %(len(ListAllRunningInstances) - len(ListAllRunningTInstances))
    print "Running instances= %d" %len(ListAllRunningInstances)
    print "Stopped instances= %d" %len(ListAllStoppedInstances)
    print "Stopped and tagged instances= %d" %len(ListAllStoppedTInstances)

#----------------------------------------------------------------------------------------------------------
    s+="\n\n Following is the instance summary for account %s" %account 
    s+= "\n\n Total Instances = %d" %len(ListAllindtance) 
    s+= "\n\n Running and tagged instances = %d" %len(ListAllRunningTInstances) 
    s+= "\n\n Running and untagged instances= %d" %(len(ListAllRunningInstances) - len(ListAllRunningTInstances)) 
    s+= "\n\n Running instances= %d" %len(ListAllRunningInstances) 
    s+= "\n\n Stopped instances= %d" %len(ListAllStoppedInstances) 
    s+= "\n\n Stopped and tagged instances= %d" %len(ListAllStoppedTInstances) 
    s+="\n\n Below is the list of instances we are going to shutdown..\n"
    #for ruinstance in ListRunningUnTaggedInstances:
    if len(ListRunningUnTaggedInstances) > 0:
            #perform the shutdown
        for instance in ListRunningUnTaggedInstances:
            s+=instance + "\n"
        print s
        #stopInstance(ListRunningUnTaggedInstances)
        publish_to_sns(s)    
    else:
        print "Nothing to see here..!"
            
def stopInstance(instanceId):
#    instanceId = ['TestingID']
    ec2.instances.filter(InstanceIds=instanceId).stop()

def publish_to_sns(message):
    sns = boto3.client('sns')
    sns_message = str(message)
    response = sns.publish(TopicArn=Topic_Arn,Subject  = "Instance Shutdown Notification of account "+ account, Message = sns_message)
