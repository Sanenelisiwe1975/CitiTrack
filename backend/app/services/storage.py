"""Cloud storage service using AWS S3"""
import boto3
from botocore.exceptions import ClientError
from ..config import settings
import uuid
from typing import Optional
import mimetypes


class StorageService:
    """Service for file storage"""
    
    def __init__(self):
        # Initialize S3 client
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.S3_REGION
            )
            self.bucket_name = settings.S3_BUCKET_NAME
            self.enabled = True
        else:
            self.s3_client = None
            self.bucket_name = None
            self.enabled = False
    
    def generate_unique_filename(self, original_filename: str) -> str:
        """Generate unique filename"""
        ext = original_filename.split('.')[-1] if '.' in original_filename else 'jpg'
        return f"reports/{uuid.uuid4()}.{ext}"
    
    async def upload_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: Optional[str] = None
    ) -> Optional[str]:
        """Upload file to S3"""
        
        if not self.enabled:
            print(f"Storage not configured, would upload: {filename}")
            return f"https://placeholder.com/{filename}"
        
        try:
            # Generate unique filename
            unique_filename = self.generate_unique_filename(filename)
            
            # Detect content type if not provided
            if not content_type:
                content_type, _ = mimetypes.guess_type(filename)
                if not content_type:
                    content_type = 'application/octet-stream'
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=unique_filename,
                Body=file_content,
                ContentType=content_type,
                ACL='public-read'  # Make publicly readable
            )
            
            # Generate public URL
            url = f"https://{self.bucket_name}.s3.{settings.S3_REGION}.amazonaws.com/{unique_filename}"
            
            return url
            
        except ClientError as e:
            print(f"S3 upload error: {e}")
            return None
    
    async def delete_file(self, file_url: str) -> bool:
        """Delete file from S3"""
        
        if not self.enabled:
            return True
        
        try:
            # Extract key from URL
            key = file_url.split('.amazonaws.com/')[-1]
            
            # Delete from S3
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=key
            )
            
            return True
            
        except ClientError as e:
            print(f"S3 delete error: {e}")
            return False
    
    def get_presigned_url(
        self,
        file_key: str,
        expiration: int = 3600
    ) -> Optional[str]:
        """Generate presigned URL for temporary access"""
        
        if not self.enabled:
            return None
        
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': file_key
                },
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            print(f"Presigned URL error: {e}")
            return None


# Singleton instance
storage_service = StorageService()