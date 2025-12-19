
import boto3

s3 = boto3.client('s3', region_name="us-east-1")
bucket = 'ds2002-f25-uzu3gv'
local_file = 'C:\\Users\\rahil\\Documents\\DS-2002-F25\\Labs\\Lab_08\\s3_bucket_lab\\cat.jpg'

with open(local_file, 'rb') as data:
    s3.put_object(
        Body=data,
        Bucket=bucket,
        Key='cat.jpg',
        ACL='public-read'
    )

print(f"https://s3.amazonaws.com/{bucket}/cat.jpg")