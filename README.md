# Balance Takehome

Balance Takehome is a prototype to connect with the [merge.dev](https://merge.dev/) Unified API to access and retrieve Accounting data from common models like Company Info, Accounts and Transactions.

## Local Requirements

- [Docker/Compose](https://docs.docker.com/engine/install/)
- [Python 3.9 or greater](https://www.python.org/downloads/)

## Local Execution

- Build images and start docker containers using:

```bash
cd balance-takehome
docker-compose up --build

access GraphiQL (Graphical interactive in-browser GraphQL IDE) through http://localhost:8000/graphql and execute the following queries:

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
```

## Technologies


## UML

Entity–relationship model

Architecture



