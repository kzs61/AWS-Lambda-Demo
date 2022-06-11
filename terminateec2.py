import boto3 

def lambda_handler(event, context):
    
    #Get list of regions
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName']
                for region in ec2_client.describe_regions()['Regions']]
                
    
    #Itirate over the regions
    for region in regions:
        ec2 = boto3.resource('ec2',region_name=region)
        
        print("Region:", region)
        
        #Get only running instances
        instances = ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name',
                        'Values': ['running']}])
                        
        #Terminate the instances
        for instance in instances:
            instance.terminate()
            print('Terminated instance:', instance.id)
