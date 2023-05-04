from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Transaction(SQLModel, table=True):
    __tablename__ = "transaction"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow)
    modified_at: datetime = Field(default=datetime.utcnow)
    name: str
    remote_id: str = Field(index=True, unique=True)
    transaction_date: datetime = Field(default=datetime.utcnow)
    transaction_to: str
    transaction_from: str
    amount: float
    currency: str
    account_id: str = Field(foreign_key="account.remote_id")
