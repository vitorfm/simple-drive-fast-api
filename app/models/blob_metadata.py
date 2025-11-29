"""Blob metadata database model."""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BlobMetadata(Base):
    """Blob metadata model."""

    __tablename__ = "blob_metadata"

    id = Column(String(255), primary_key=True)
    size = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    storage_backend = Column(String(50), nullable=False)
    storage_path = Column(String(512), nullable=True)

