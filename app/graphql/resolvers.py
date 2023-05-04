from graphene import Date, Field, Int, List, ObjectType

from app.graphql.schemas.balance_breakdown import (
    BalanceBreakdown,
    BankAccount,
    DateTimeType,
)
from app.graphql.schemas.income_and_expenses import IncomeExpenses
from app.graphql.schemas.transaction import TransactionsList
from app.utils.formatter import FormatterUtil


class BankQuery(ObjectType):
    bank_accounts = List(BankAccount)

    def resolve_bank_accounts(self, info):
        return FormatterUtil().get_bank_schemas()


class TransactionsQuery(ObjectType):
    transactions = List(TransactionsList)

    def resolve_transactions(self, info, start_date, end_date):
        return FormatterUtil().get_transactions_for_interval_schema(
            start_date, end_date
        )


class Query(ObjectType):
    balance_breakdown = List(BalanceBreakdown)
    income_and_expenses = Field(
        IncomeExpenses, month=Int(required=True), year=Int(required=True)
    )
    transactions_for_interval = Field(
        TransactionsList, start_date=Date(required=True), end_date=Date(required=True)
    )

    def resolve_balance_breakdown(self, info):
        return [DateTimeType(), BankQuery.resolve_bank_accounts(None, info)]

    def resolve_income_and_expenses(self, info, month, year):
        return FormatterUtil().get_income_expense_schema(month, year)

    def resolve_transactions_for_interval(self, info, start_date, end_date):
        return TransactionsQuery.resolve_transactions(None, info, start_date, end_date)
