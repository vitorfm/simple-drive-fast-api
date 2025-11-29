from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.storage.base import StorageBackend
from app.storage.database import DatabaseStorageBackend
from app.storage.local import LocalStorageBackend
from app.storage.s3_compatible import S3CompatibleStorageBackend
from app.utils.exceptions import StorageBackendError


async def get_storage_backend(db_session: AsyncSession) -> StorageBackend:
    if settings.storage_backend == "local":
        return LocalStorageBackend(settings.local_storage_path)
    elif settings.storage_backend == "database":
        return DatabaseStorageBackend(db_session)
    elif settings.storage_backend == "s3":
        if not all([settings.s3_endpoint_url, settings.s3_access_key_id, settings.s3_secret_access_key, settings.s3_bucket_name]):
            raise StorageBackendError("S3 configuration incomplete. Required: endpoint_url, access_key_id, secret_access_key, bucket_name")
        return S3CompatibleStorageBackend(
            settings.s3_endpoint_url,
            settings.s3_bucket_name,
            settings.s3_access_key_id,
            settings.s3_secret_access_key,
            settings.s3_region,
        )
    elif settings.storage_backend == "ftp":
        raise StorageBackendError("FTP storage backend not implemented yet")
    else:
        raise StorageBackendError(f"Unknown storage backend: {settings.storage_backend}")

