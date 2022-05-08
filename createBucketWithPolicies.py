import argparse
import json
import time
from os import getenv
from pprint import pprint

import boto3
import botocore.exceptions

AWS_REGION = getenv("AWS_REGION", "us-east-1")
s3_client=boto3.client("s3", region_name=AWS_REGION)

def bucket_exists(bucket_name):
    try:
        response = s3_client.head_bucket(Bucket=bucket_name)
        print("bucket already exists")
    except botocore.exceptions.ClientError as e:
        return False
    status_code=response["ResponseMetadata"]["HTTPStatusCode"]
    if status_code==200:
        return True
    return False

def create_bucket(bucket_name):
    if not bucket_exists(bucket_name):
        try:
            s3_client.create_bucket(Bucket=bucket_name)
            print(f"bucket '{bucket_name} 'created successfully")
        except botocore.exceptions.ClientError as e:
            print(e)

def generate_policy(bucket_name):
    Policy= {
        "Version" : "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/*"

            }
        ]
    }
    return json.dumps(Policy)

def create_policy(bucket_name):
    try:
        s3_client.put_bucket_policy(Bucket=bucket_name, Policy=generate_policy(bucket_name))
    except botocore.exceptions.ClientError as e:
        print(e)

def set_website_configuration(bucket_name):
    response=s3_client.put_bucket_website(
        Bucket=bucket_name,
        WebsiteConfiguration={
            'ErrorDocument': {
                'Key': 'error.html'
            },
            'IndexDocument': {
                'Suffix': 'index.html'
            }
        }
    )
    pprint(response)

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-b", "--bucket", type=str, required=True)
    args=parser.parse_args()
    return args

def main():
    args=parse_args()
    create_bucket(args.bucket)
    time.sleep(15)
    create_policy(args.bucket)
    set_website_configuration(args.bucket)


if __name__ == '__main__':
    main()

