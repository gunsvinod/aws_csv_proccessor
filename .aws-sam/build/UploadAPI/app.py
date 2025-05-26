import json
import boto3
import os
import base64

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    body = json.loads(event['body'])
    file_name = body['filename']
    file_content = base64.b64decode(body['file'])

    s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=file_content)

    return {
        'statusCode': 200,
        'body': json.dumps({'message': f'File {file_name} uploaded to S3'})
    }
