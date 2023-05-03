from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Company(SQLModel, table=True):
    __tablename__ = "company"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow)
    modified_at: datetime = Field(default=datetime.utcnow)
    legal_name: str
    name: str
    remote_id: str = Field(index=True, unique=True)
    tax_number: Optional[str]
    fiscal_year_end_day: Optional[int]
    fiscal_year_end_month: Optional[int]
    currency: str
