from app.database.repository import (
    AccountRepository,
    CompanyRepository,
    SyncStatusRepository,
    TransactionRepository,
)


class BaseUtil:
    """
    BaseUtil Class that accesses different db repositories.
    """

    def __init__(self):
        self.account_repository = AccountRepository()
        self.company_repository = CompanyRepository()
        self.transaction_repository = TransactionRepository()
        self.sync_status_repository = SyncStatusRepository()
