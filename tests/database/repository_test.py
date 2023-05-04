from tests.fixtures import create_test_company


def test_company(create_test_company):
    company = create_test_company()
    assert company.legal_name == "My Company Legal Name"
