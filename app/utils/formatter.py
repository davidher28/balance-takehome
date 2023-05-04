import calendar
from datetime import date

from app.graphql.schemas.balance_breakdown import BankAccountsList
from app.graphql.schemas.income_and_expenses import IncomeExpenses
from app.graphql.schemas.transaction import TransactionsList
from app.utils import BaseUtil


class FormatterUtil(BaseUtil):
    def __init__(self):
        super().__init__()

    def get_bank_schemas(self) -> BankAccountsList:
        accounts = self.account_repository.get_by_account_type("Bank")
        return BankAccountsList(accounts=accounts)

    def get_income_expense_schema(self, month: int, year: int) -> IncomeExpenses:
        start_date = date(year, month, 1)
        _, num_days = calendar.monthrange(year, month)
        end_date = date(year, month, num_days)
        transactions = self.transaction_repository.get_for_interval(
            start_date=start_date, end_date=end_date
        )
        return IncomeExpenses(income=314, expenses=231)

    def get_transactions_for_interval_schema(
        self, start_date: date, end_date: date
    ) -> TransactionsList:
        transactions = self.transaction_repository.get_for_interval(
            start_date=start_date, end_date=end_date
        )
        return TransactionsList(transactions=transactions)
