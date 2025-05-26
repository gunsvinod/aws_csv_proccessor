import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')
secrets = boto3.client('secretsmanager')

def get_secret():
    secret = secrets.get_secret_value(SecretId=os.environ['SECRET_NAME'])
    return json.loads(secret['SecretString'])

def lambda_handler(event, context):
    secret = get_secret()
    table = dynamodb.Table(secret['DYNAMODB_TABLE'])

    for record in event['Records']:
        item = json.loads(record['body'])
        table.put_item(Item=item)
