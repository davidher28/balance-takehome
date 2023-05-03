from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Account(SQLModel, table=True):
    __tablename__ = "account"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow)
    modified_at: datetime = Field(default=datetime.utcnow)
    name: str
    remote_id: str = Field(index=True, unique=True)
    account_type: str
    classification: str
    status: str
    current_balance: float
    currency: str
    company_id: str = Field(foreign_key="company.remote_id")
