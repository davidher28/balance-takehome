

alembic init alembic

docker-compose run app alembic revision --autogenerate
docker-compose run app alembic upgrade head

docker-compose run app pytest
docker-compose run app black main.py app tests
docker-compose run app isort main.py app tests
docker-compose run app mypy main.py app tests

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
  transactionsForInterval(startDate:"2023-01-01", endDate:"2023-04-01") {
    ... on TransactionsList {
      transactions {        
        date
        name
        transactionTo
        transactionFrom
        amount
      }
    }
  }
}
