from datetime import timedelta
from io import BytesIO

from minio import Minio

from app.config import settings


class ObjectStorage:
    def __init__(self):
        self.client = Minio(
            settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_secure,
        )
        self.bucket = settings.minio_bucket

    def ensure_bucket(self):
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

    def upload_bytes(self, object_name: str, content: bytes, content_type: str):
        self.ensure_bucket()
        self.client.put_object(
            self.bucket,
            object_name,
            BytesIO(content),
            length=len(content),
            content_type=content_type,
        )

    def presigned_download_url(self, object_name: str, expires_seconds: int) -> str:
        self.ensure_bucket()
        return self.client.presigned_get_object(
            self.bucket,
            object_name,
            expires=timedelta(seconds=expires_seconds),
        )


_storage = ObjectStorage()


def get_storage() -> ObjectStorage:
    return _storage
