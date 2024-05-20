import json
import boto3
import time

# TODO リファクタ(実装、メッセージ)
def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # イベントからアクションとインスタンスIDを取得
    action = event.get('queryStringParameters').get('action')
    instance_id = 'xxxxxx'
    
    # CORSを許可する

    if not action or not instance_id:
        return {
            'statusCode': 400,
            'headers' : {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": '*'
            },
            'body': json.dumps('Missing action or instance_id in request')
        }
    
    try:
        if action == 'start':
            # インスタンスを起動
            response = ec2.start_instances(InstanceIds=[instance_id])
            # インスタンスの起動を待機する
            instance_running = False
            while not instance_running:
               instance = ec2.describe_instances(InstanceIds=[instance_id])
               state = instance['Reservations'][0]['Instances'][0]['State']['Name']
               if state == 'running':
                  instance_running = True
               else:
                  time.sleep(5)
            # public ipを取得
            instance = ec2.describe_instances(InstanceIds=[instance_id])
            public_ip = instance['Reservations'][0]['Instances'][0]['PublicIpAddress']
            print(f'EC2 Instance {instance_id} started successfully')
            return {
                'statusCode': 200,
                'headers' : {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": '*'
                },
                'body': json.dumps(f'Minecraft EC2 Instance {instance_id} started successfully at {public_ip}:25565')
            }
        
        elif action == 'stop':
            # インスタンスを停止
            response = ec2.stop_instances(InstanceIds=[instance_id])
            ec2.describe_instances(InstanceIds=[instance_id])
            print(f'EC2 Instance {instance_id} stopped successfully')
            return {
                'statusCode': 200,
                'headers' : {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": '*'
                },
                'body': json.dumps(f'EC2 Instance {instance_id} stopped successfully')
            }
        
        else:
            return {
                'statusCode': 400,
                'headers' : {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": '*'
                },
                'body': json.dumps('Invalid action')
            }
    
    except Exception as e:
        print(f'Error with action {action} on EC2 Instance: {e}')
        return {
            'statusCode': 500,
            'headers' : {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": '*'
            },
            'body': json.dumps(f'Error with action {action} on EC2 Instance: {e}')
        }