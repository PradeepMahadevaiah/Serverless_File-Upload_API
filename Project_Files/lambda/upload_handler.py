import json
import boto3
import base64
import os
from urllib.parse import unquote_plus

s3 = boto3.client('s3')
BUCKET_NAME = os.environ.get('UPLOAD_BUCKET')

def lambda_handler(event, context):
    try:
        body = event['body']
        is_base64_encoded = event.get('isBase64Encoded', False)

        if is_base64_encoded:
            decoded = base64.b64decode(body)
        else:
            decoded = body.encode('utf-8')

        filename = event['headers'].get('X-Filename', 'uploaded_file')
        s3.put_object(Bucket=BUCKET_NAME, Key=filename, Body=decoded)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Upload successful', 'filename': filename})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error uploading file', 'error': str(e)})
        }
