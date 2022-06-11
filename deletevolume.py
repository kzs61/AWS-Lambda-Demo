import boto3

def lambda_handler(event, context):
    
    
    #Get list of regions
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName']
                for region in ec2_client.describe_regions()['Regions']]
                
    
    for region in regions:
        ec2 = boto3.resource('ec2', region_name=region)
        print(f"List all AWS regions for visibility: {region}")
        
        #List only unattached volumes ('available' vs 'in-use')
        volumes = ec2.volumes.filter(Filters=[{'Name': 'status','Values': ['available']}])
        
        #Remove volumes
        for volume in volumes:
            v = ec2.Volume(volume.id)
            print('Deleting EBS Volume: {}, Size: {} GiB'.format(v.id, v.size))
            v.delete()
