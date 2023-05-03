from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class SyncStatus(SQLModel, table=True):
    __tablename__ = "sync_status"

    id: Optional[int] = Field(default=None, primary_key=True)
    last_sync_at: datetime = Field(default=datetime.utcnow)
