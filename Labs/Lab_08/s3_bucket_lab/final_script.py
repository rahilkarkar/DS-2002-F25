import boto3
import urllib.request

url = 'https://httpbin.org/image/jpeg'
filename = 'downloaded.jpg'
urllib.request.urlretrieve(url, filename)

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'ds2002-f25-uzu3gv'

with open(filename, 'rb') as data:
    s3.put_object(Body=data, Bucket=bucket, Key=filename)

presigned_url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': bucket, 'Key': filename},
    ExpiresIn=604800
)

print(presigned_url)