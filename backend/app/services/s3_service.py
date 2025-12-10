import boto3
import hashlib

from io import BytesIO
from botocore.exceptions import ClientError
from app.core.config import settings

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.S3_ENDPOINT_URL
        )
        self.bucket_name = settings.S3_BUCKET_NAME
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':  # Only create if bucket doesn't exist
                try:
                    self.s3_client.create_bucket(Bucket=self.bucket_name)
                except ClientError as create_error:
                    print(f"Failed to create bucket: {create_error}")

    async def upload_image(self, file_bytes: bytes, file_name: str, content_type: str, username: str) -> str:
        file_hash = hashlib.sha256(file_bytes).hexdigest()
        file_ext = file_name.split('.')[-1]
        s3_key = f"{username}/{file_hash}.{file_ext}"

        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=BytesIO(file_bytes),
                ContentType=content_type
            )
            return s3_key
        except ClientError as e:
            raise Exception(f"Failed to upload file to S3: {e}")