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
  managed=[]
  for computer in response['computers']:
    if computer['computerStatus']['agentStatusMessages'] == ["Managed (Online)"] :
      managed.append(computer['ec2VirtualMachineSummary']['instanceID'])
            
  described = ec2.describe_instances(InstanceIds=managed)
            
  critical_windows=[]
  critical_linux=[]
  for instance in described['Reservations']:
    if instance['Instances'][0].get('Platform') is not None:
      critical_windows.append(instance['Instances'][0]['InstanceId'])
    else:
      critical_linux.append(instance['Instances'][0]['InstanceId'])
            
  instancestountagwindows = [value for value in managed if value in critical_windows]
  instancestountaglinux = [value for value in managed if value in critical_linux]    
            
  if instancestountaglinux:
    response = ec2.delete_tags(Resources=instancestountaglinux , Tags=[{'Key':'DSA', 'Value':'LinuxAgentRequired'}])
    response = ec2.create_tags(Resources=instancestountaglinux , Tags=[{'Key':'DSA', 'Value':'LinuxAgentInstalled'}])
            
  if instancestountagwindows:
    response = ec2.delete_tags(Resources=instancestountagwindows , Tags=[{'Key':'DSA', 'Value':'WindowsAgentRequired'}])
    response = ec2.create_tags(Resources=instancestountagwindows , Tags=[{'Key':'DSA', 'Value':'WindowsAgentInstalled'}])