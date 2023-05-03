# Balance Takehome

Balance Takehome is a prototype GraphQL API to connect with the [merge.dev](https://merge.dev/) Unified API to access and retrieve ```Accounting``` data from common models like ```Company Info```, ```Accounts``` and ```Transactions```.

## Local Requirements

- [Docker/Compose](https://docs.docker.com/engine/install/)
- [Python 3.9 or greater](https://www.python.org/downloads/)

## Local Execution

- Build images and start docker containers using:

```bash
cd balance-takehome
docker-compose up --build
```

- Access GraphiQL (In-Browser GraphQL IDE) through http://localhost:8000/graphql and execute the following queries:

```bash
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

## Local Development

- Execute the unit tests session through ```pytest```:

```bash
docker-compose run app pytest
```

- Execute the ```Black``` python formatter:

```bash
docker-compose run app black main.py app tests
```

- Execute the ```isort``` utility to manage imports across the app:

```bash
docker-compose run app isort main.py app tests
```

- Execute the static type checking analysis using ```mypy```:

```bash
docker-compose run app mypy main.py app tests
```

- After any database schema/tables change, you'd have to execute the following migration commands:

```bash
docker-compose run app alembic revision --autogenerate
docker-compose run app alembic upgrade head
```

## Technologies / Tradeoffs

### FastAPI
- FastAPI provides high performance and good coding time. Also, through its async capabilities and web server (ASGI Standard - Asynchronous Server Gateway Interface), we can schedule a coroutine that executes the polling process with real time confidence just as a Celery task.

### PostgreSQL
- PostgreSQL is widely used as a relational database for API's supported by ORM's to abstract the interaction. Using it we gain flexibility and particular capabilities/utilities like the ```on_conflict_do_update``` method to execute the ```UPSERT``` operation using constraints.

### SQLModel - SQLAlchemy & Pydantic
- The SQLModel library mixes the features from SQLAlchemy & Pydantic. It provides a layer of communication (between both libraries) that allows the creation of database tables through type annotations, just as simple as a ```dataclass``` or a Pydantic ```BaseModel```. Avoiding code duplication and supporting a clean codebase.

## UML

### Entity–relationship model


### Architecture



