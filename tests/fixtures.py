from datetime import datetime

import pytest

from app.models.company import Company


@pytest.fixture(scope="function")
def create_test_company(db_session):
    def inner_func() -> Company:
        company = Company(
            remote_id="dbf99e9f-dbf99e9f-dbf99e9f",
            created_at=datetime.utcnow,
            legal_name="My Company Legal Name",
            name="My Company Name",
            tax_number="432fds2",
            fiscal_year_end_day=15,
            fiscal_year_end_month=10,
            currency="USD",
        )
        db_session.add(company)
        db_session.flush()
        return company

    return inner_func
