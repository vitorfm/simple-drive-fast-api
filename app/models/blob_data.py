from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, LargeBinary, String
from sqlalchemy.ext.declarative import declarative_base

from app.models.blob_metadata import Base


class BlobData(Base):
    __tablename__ = "blob_data"

    id = Column(String(255), primary_key=True)
    data = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

