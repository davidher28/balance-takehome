import contextlib

import pytest
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
from sqlmodel import Session, SQLModel, create_engine

from app.database.session import engine
from app.settings import settings


@pytest.fixture(scope="session")
def db_connection(request):
    """
    Connection used to create and drop the isolated testing DB.
    """

    connection = engine.connect()
    connection.execution_options(isolation_level="AUTOCOMMIT")

    with contextlib.suppress(ProgrammingError):
        connection.execute(text(f"CREATE DATABASE {settings.test_db_name};"))

    def teardown():
        connection.execute(text(f"DROP DATABASE {settings.test_db_name} WITH (FORCE);"))
        connection.close()

    request.addfinalizer(teardown)

    test_engine = create_engine(f"{settings.db_url}/{settings.test_db_name}")
    return test_engine.connect()


@pytest.fixture(scope="session", autouse=True)
def db_setup(db_connection, request):
    """
    Models setup and creation.
    """
    SQLModel.metadata.bind = db_connection
    SQLModel.metadata.create_all()

    def teardown():
        SQLModel.metadata.drop_all()

    request.addfinalizer(teardown)


@pytest.fixture(scope="function", autouse=True)
def db_session(db_connection, request):
    """
    Session used to execute commands through the current connection with the isolated testing DB.
    """
    session = Session(bind=db_connection)
    session.begin_nested()

    def teardown():
        db_connection.rollback()

    request.addfinalizer(teardown)
    return session
