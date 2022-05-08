import argparse
import mimetypes
import os
from os import getenv
import boto3
AWS_REGION=getenv("AWS_REGION", "us-east-1")
s3_client=boto3.client("s3", region_name=AWS_REGION)

def guess_type(path):
    mimetype, _ =mimetypes.guess_type(path)
    if mimetype is None:
        return "binary/octet-stream"
    return mimetype

def upload_dir(path, bucket_name):
    for root, _ , files in os.walk(path):
        for file in files:
            file_path=os.path.join(root, file)
            s3_client.upload_file(file_path,
                                  bucket_name,
                                  file_path.replace(f"{path}/", ""),
                                  ExtraArgs={
                                      "ContentType": guess_type(file_path)
                                  }
                                  )



def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-b", "--bucket",type=str,required=True)
    parser.add_argument("-d", "--dir",type=str,required=True)
    args=parser.parse_args()
    return args

def main():

    args=parse_args()
    upload_dir(args.dir, args.bucket)



if __name__ == '__main__':
    main()