import json
import boto3
import time

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    instance_id = 'i-0d0aea6608cc02315'
    
    # インスタンス情報を取得
    instance = ec2.describe_instances(InstanceIds=[instance_id])
    state = instance['Reservations'][0]['Instances'][0]['State']['Name']
    
    message = 'minecraft server is currently not running'
    
    if state == 'running':
        public_ip = instance['Reservations'][0]['Instances'][0]['PublicIpAddress']
        message = f'minecraft is currently running at {public_ip}:25565'
    
    # TODO implement
    return {
        'statusCode': 200,
        'headers' : {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": '*'
        },
        'body': json.dumps(message)
    }
