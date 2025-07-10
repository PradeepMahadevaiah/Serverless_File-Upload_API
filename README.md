# Serverless File Upload API with AWS Lambda, API Gateway, and S3

This project demonstrates how to build a **serverless file upload API** using AWS services including **API Gateway**, **Lambda (Python)**, and **S3**, along with a simple **HTML frontend**.

---

## 📌 Overview
- Users upload files from a browser
- The frontend calls a REST API hosted on **API Gateway**
- The request is processed by a **Lambda function**
- The file is stored securely in an **S3 bucket**

---

## 🛠️ Tech Stack
- **AWS Lambda (Python)**
- **Amazon API Gateway**
- **Amazon S3**
- **CloudFormation/SAM**
- **HTML + JavaScript**

---

## 📁 Folder Structure
```
serverless-file-uploader/
├── frontend/
│   └── index.html         # Upload form
├── lambda/
│   └── upload_handler.py  # Lambda handler for file upload
├── template.yaml          # AWS SAM/CloudFormation template
└── README.md
```

---

## 🚀 How It Works
1. User selects a file on the HTML page
2. JS fetch() makes a POST request to the API Gateway URL
3. API Gateway triggers Lambda with the file data
4. Lambda uploads file to S3 using `boto3`

---

## 🌐 API Endpoint
After deployment, your file upload endpoint will look like:
```
https://<api-id>.execute-api.<region>.amazonaws.com/Prod/upload
```

Replace this in `index.html` before testing:
```js
const response = await fetch("YOUR_API_GATEWAY_ENDPOINT", {
```

---

## 🔧 Setup Instructions

### Prerequisites
- AWS CLI configured with access
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- S3 bucket will be created by template

### 1. Deploy with AWS SAM
```bash
sam build
sam deploy --guided
```
Follow prompts to:
- Set stack name
- Select AWS region
- Confirm S3 bucket creation

### 2. Update `index.html`
Replace `YOUR_API_GATEWAY_ENDPOINT` with your real API Gateway endpoint output from the SAM deployment.

---

## 🐍 Lambda Handler (`upload_handler.py`)
```python
import json
import boto3
import base64
import os

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
```

---

## 📸 Screenshots (Add these when available)
- Upload page interface
- File chosen in browser
- S3 bucket with uploaded file
- API Gateway & Lambda test logs

---

## ✅ TODO
- [ ] Add client-side file type/size validation
- [ ] Secure API with IAM or Cognito
- [ ] Log uploads to DynamoDB

---

## 👨‍💻 Author
**Pradeep Mahadevaiah**  
DevOps | Cloud | AWS | Automation  
GitHub: [github.com/PradeepMahadevaiah](https://github.com/PradeepMahadevaiah)

---

## 📝 License
MIT License
