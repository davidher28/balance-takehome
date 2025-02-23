# Balance Takehome 💰

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

- Access pgAdmin through http://localhost:5050 to verify the schema creation and the ingested data:

![alt text](https://github.com/davidher28/balance-takehome/blob/main/static/pgAdmin2.png)

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
```

![alt text](https://github.com/davidher28/balance-takehome/blob/main/static/graphiql.png)

## Local Development

- Execute the unit tests session through ```pytest```:

```bash
docker exec balance_takehome_app pytest
```

- Execute the pre-configured ```Black``` python formatter:

```bash
docker exec balance_takehome_app black main.py app tests
```

- Execute the ```isort``` utility to manage imports:

```bash
docker exec balance_takehome_app isort main.py app tests
```

- Execute a static type checking analysis using ```mypy```:

```bash
docker exec balance_takehome_app mypy main.py app tests
```

- After any database schema/tables change, you'd have to execute the following migration commands:

```bash
docker exec balance_takehome_app alembic revision --autogenerate
docker exec balance_takehome_app alembic upgrade head
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

![alt text](https://github.com/davidher28/balance-takehome/blob/main/static/ER-Model.png)

### Architecture

![alt text](https://github.com/davidher28/balance-takehome/blob/main/static/architecture.png)

