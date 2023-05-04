from datetime import datetime

from graphene import DateTime, Float, List, ObjectType, String, Union


class Transaction(ObjectType):
    transaction_date = DateTime()
    name = String()
    transaction_to = String()
    transaction_from = String()
    amount = Float()


class TransactionsList(ObjectType):
    transactions = List(Transaction)

    def resolve_transactions(self, info):
        return self.transactions
