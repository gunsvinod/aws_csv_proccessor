import boto3
import csv
import os
import json

s3 = boto3.client('s3')
sqs = boto3.client('sqs')
secrets = boto3.client('secretsmanager')

def get_secret():
    secret = secrets.get_secret_value(SecretId=os.environ['SECRET_NAME'])
    return json.loads(secret['SecretString'])

def lambda_handler(event, context):
    secret = get_secret()
    queue_url = secret['SQS_QUEUE_URL']

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        obj = s3.get_object(Bucket=bucket, Key=key)
        lines = obj['Body'].read().decode('utf-8').splitlines()
        reader = csv.DictReader(lines)

        for row in reader:
            sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(row))
