from datetime import date, datetime

from app.database.repository import (AccountRepository, CompanyRepository,
                                     SyncStatusRepository,
                                     TransactionRepository)
from app.graphql.schemas.balance_breakdown import BankAccountsList
from app.graphql.schemas.income_and_expenses import IncomeExpenses
from app.graphql.schemas.transaction import Transaction, TransactionsList
from app.utils import BaseUtil


class FormatterUtil(BaseUtil):
    def __init__(self):
        super().__init__()

    def get_bank_schemas(self) -> BankAccountsList:
        accounts = self.account_repository.get_by_account_type("Bank")
        return BankAccountsList(accounts=accounts)

    def get_income_expense_schema(self, month: float, year: float) -> IncomeExpenses:
        return IncomeExpenses(income=314, expenses=231)

    def get_transactions_for_interval_schema(
        self, start_date: date, end_date: date
    ) -> TransactionsList:
        # transactions = self.transaction_repository.get_for_interval(start_date=start_date, end_date=end_date)
        return TransactionsList(
            transactions=[
                Transaction(datetime.utcnow(), "name", "name_to", "name_from", 43324),
                Transaction(datetime.utcnow(), "name", "name_to", "name_from", 43324),
                Transaction(datetime.utcnow(), "name", "name_to", "name_from", 43324),
                Transaction(datetime.utcnow(), "name", "name_to", "name_from", 43324),
                Transaction(datetime.utcnow(), "name", "name_to", "name_from", 43324),
            ]
        )
