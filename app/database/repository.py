from datetime import datetime
from typing import Optional

from sqlalchemy.dialects.postgresql import insert

from app.database.session import db_session
from app.models.account import Account
from app.models.company import Company
from app.models.sync_status import SyncStatus
from app.models.transaction import Transaction


class AccountRepository:
    """
    Account Repository to access and create __account__ data.
    """

    def add_batch(self, account_values: list[dict]) -> None:
        insert_stmt = insert(Account).values(account_values)
        upsert_statement = insert_stmt.on_conflict_do_update(
            index_elements=["remote_id"],
            set_={
                "created_at": insert_stmt.excluded.created_at,
                "modified_at": insert_stmt.excluded.modified_at,
                "name": insert_stmt.excluded.name,
                "account_type": insert_stmt.excluded.account_type,
                "classification": insert_stmt.excluded.classification,
                "status": insert_stmt.excluded.status,
                "current_balance": insert_stmt.excluded.current_balance,
                "currency": insert_stmt.excluded.currency,
            },
        )
        db_session.execute(upsert_statement)
        db_session.commit()

    def get(self, remote_id: str) -> Optional[Company]:
        query = db_session.query(Company).filter(Company.remote_id == remote_id)
        return query.first()

    def get_by_account_type(self, account_type: str):
        query = db_session.query(Account).filter(Account.account_type == account_type)
        return query.all()


class CompanyRepository:
    """
    Company Repository to access and create __company__ data.
    """

    def add_batch(self, company_values: list[dict]) -> None:
        insert_stmt = insert(Company).values(company_values)
        upsert_statement = insert_stmt.on_conflict_do_update(
            index_elements=["remote_id"],
            set_={
                "created_at": insert_stmt.excluded.created_at,
                "modified_at": insert_stmt.excluded.modified_at,
                "legal_name": insert_stmt.excluded.legal_name,
                "name": insert_stmt.excluded.name,
                "tax_number": insert_stmt.excluded.tax_number,
                "fiscal_year_end_day": insert_stmt.excluded.fiscal_year_end_day,
                "fiscal_year_end_month": insert_stmt.excluded.fiscal_year_end_month,
                "currency": insert_stmt.excluded.currency,
            },
        )
        db_session.execute(upsert_statement)
        db_session.commit()

    def get(self, remote_id: str) -> Optional[Company]:
        query = db_session.query(Company).filter(Company.remote_id == remote_id)
        return query.first()

    def get_batch(self, remote_ids: list[int]):
        query = db_session.query(Company).filter(Company.remote_id.in_(remote_ids))
        return query.all()


class SyncStatusRepository:
    """
    SyncStatus Repository to access and create __sync_status__ data.
    """

    def add(self) -> SyncStatus:
        sync_status = SyncStatus(last_sync_at=datetime.utcnow())
        db_session.add(sync_status)
        db_session.commit()
        return sync_status

    def get(self) -> Optional[SyncStatus]:
        query = db_session.query(SyncStatus).order_by(SyncStatus.last_sync_at.desc())
        return query.first()


class TransactionRepository:
    """
    Transaction Repository to access and create __transaction__ data.
    """

    def add_batch(self, transaction_values: list[dict]) -> None:
        insert_stmt = insert(Transaction).values(transaction_values)
        upsert_statement = insert_stmt.on_conflict_do_update(
            index_elements=["remote_id"],
            set_={
                "created_at": insert_stmt.excluded.created_at,
                "modified_at": insert_stmt.excluded.modified_at,
                "name": insert_stmt.excluded.name,
                "transaction_date": insert_stmt.excluded.transaction_date,
                "transaction_to": insert_stmt.excluded.transaction_to,
                "transaction_from": insert_stmt.excluded.transaction_from,
                "amount": insert_stmt.excluded.amount,
                "currency": insert_stmt.excluded.currency,
            },
        )
        db_session.execute(upsert_statement)
        db_session.commit()
