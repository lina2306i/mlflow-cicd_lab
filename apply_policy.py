import boto3
import json

s3 = boto3.client('s3', endpoint_url='http://127.0.0.1:9000', 
                  aws_access_key_id='root', aws_secret_access_key='root123456789')

policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": ["*"]},
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::mlflow",
                "arn:aws:s3:::mlflow/*"
            ]
        }
    ]
}


s3.put_bucket_policy(Bucket='mlflow', Policy=json.dumps(policy))
print("Succès !")
