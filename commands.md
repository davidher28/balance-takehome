

alembic init alembic

docker exec balance_takehome_app alembic revision --autogenerate
docker exec balance_takehome_app alembic upgrade head

docker exec balance_takehome_app pytest
docker exec balance_takehome_app black main.py app tests
docker exec balance_takehome_app isort main.py app tests
docker exec balance_takehome_app mypy main.py app tests

GraphQL Queries:

1.
query {
  balanceBreakdown {
      ... on DateTimeType {
          now
      }
      ... on BankAccountsList {
        accounts {
          name
          currentBalance
        }
      }
  }
}

2.
query {
  incomeAndExpenses(month:10, year:2023) {
    income
    expenses
  }
}

3.
query {
  transactionsForInterval(startDate:"2023-03-01", endDate:"2023-03-21") {
    ... on TransactionsList {
      transactions {        
        transactionDate
        name
        transactionTo
        transactionFrom
        amount
      }
    }
  }
}
