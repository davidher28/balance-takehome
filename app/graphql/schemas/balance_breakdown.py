from datetime import datetime

from graphene import DateTime, Float, List, ObjectType, String, Union


class BankAccount(ObjectType):
    name = String()
    current_balance = Float()


class BankAccountsList(ObjectType):
    accounts = List(BankAccount)

    def resolve_accounts(self, info):
        return self.accounts


class DateTimeType(ObjectType):
    now = DateTime()

    def resolve_now(self, info):
        return datetime.now()


class BalanceBreakdown(Union):
    class Meta:
        types = (DateTimeType, BankAccountsList)
