import json
from botocore.vendored import requests
import boto3
import os
          
ec2 = boto3.client('ec2')
def lambda_handler(event, context):
  url = "https://cloudone.trendmicro.com/api/computers?computerStatus"
  headers = {
    'api-version': "v1",
    'api-secret-key': os.environ.get('apisecret')
    }
  response = requests.get(url, headers=headers).json()
            
  filters = [{
    'Name': 'tag:Severity',
    'Values': ['CRITICAL']
     }
     ]
              
  unmanaged=[]
  for computer in response['computers']:
    if computer['computerStatus']['agentStatusMessages'] == ["Unmanaged (Unknown)"] :
      unmanaged.append(computer['ec2VirtualMachineSummary']['instanceID'])
                
  described = ec2.describe_instances(Filters=filters)
            
  critical_windows=[]
  critical_linux=[]
  for instance in described['Reservations']:
    if instance['Instances'][0].get('Platform') is not None:
      critical_windows.append(instance['Instances'][0]['InstanceId'])
    else:
      critical_linux.append(instance['Instances'][0]['InstanceId'])
            
  instancestotagwindows = [value for value in unmanaged if value in critical_windows]
  instancestotaglinux = [value for value in unmanaged if value in critical_linux]
            
  if instancestotagwindows:
    response = ec2.create_tags(Resources=instancestotagwindows , Tags=[{'Key':'DSA', 'Value':'WindowsAgentRequired'}])
  if instancestotaglinux:
    response = ec2.create_tags(Resources=instancestotaglinux , Tags=[{'Key':'DSA', 'Value':'LinuxAgentRequired'}])