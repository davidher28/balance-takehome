from datetime import datetime

from graphene import DateTime, Float, List, ObjectType, String, Union


class IncomeExpenses(ObjectType):
    income = Float()
    expenses = Float()
