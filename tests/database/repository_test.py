from app.database.repository import CompanyRepository


def test_company(create_test_company):
    company = create_test_company()
    assert company.legal_name == "My Company Legal Name"
