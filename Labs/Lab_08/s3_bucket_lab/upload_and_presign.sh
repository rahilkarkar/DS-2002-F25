#!/bin/bash

if [ $# -ne 3 ]; then
    echo "Usage: $0 <local_file> <bucket_name> <expiration_seconds>"
    exit 1
fi

LOCAL_FILE=$1
BUCKET_NAME=$2
EXPIRATION=$3

echo "Uploading $LOCAL_FILE to s3://$BUCKET_NAME/..."
aws s3 cp "$LOCAL_FILE" "s3://$BUCKET_NAME/"

if [ $? -eq 0 ]; then
    echo "Upload successful!"
    
    echo "Generating presigned URL (expires in $EXPIRATION seconds)..."
    PRESIGNED_URL=$(aws s3 presign --expires-in "$EXPIRATION" "s3://$BUCKET_NAME/$(basename $LOCAL_FILE)")
    
    echo "Presigned URL:"
    echo "$PRESIGNED_URL"
else
    echo "Upload failed!"
    exit 1
fi