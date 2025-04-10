from io import BytesIO
import boto3
import uuid

s3 = boto3.client(
    "s3",
    endpoint_url="http://minio:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
)

bucket_name = "documents"

# Ensure bucket exists
try:
    s3.head_bucket(Bucket=bucket_name)
except:
    s3.create_bucket(Bucket=bucket_name)

def upload_to_minio(filename: str, content: bytes) -> str:
    # Create a unique file ID but keep original filename
    file_id = f"{uuid.uuid4()}_{filename}"

    s3.upload_fileobj(
        Fileobj=BytesIO(content),
        Bucket=bucket_name,
        Key=file_id,
        ExtraArgs={"ContentType": "application/pdf"}  # Important!
    )
    return file_id
