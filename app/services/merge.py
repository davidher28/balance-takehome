from datetime import datetime
from pprint import pprint
from typing import Callable, Iterator, Optional

import MergeAccountingClient
from MergeAccountingClient import ApiException
from MergeAccountingClient.api import (accounts_api, company_info_api,
                                       expenses_api, income_statements_api,
                                       sync_status_api, transactions_api)

from app.settings import settings


class MergeAccounting:
    """
    Service Class that allows communication with merge.dev and their synced data using the MergeAccountingClient SDK.
    """

    def __init__(
        self, accounting_auth_key: str, x_account_token: str, remote_company_id: str
    ):
        config = MergeAccountingClient.Configuration()
        config.api_key_prefix["tokenAuth"] = "Bearer"
        config.api_key["tokenAuth"] = accounting_auth_key
        self._accounting_client = MergeAccountingClient.ApiClient(config)
        self._x_account_token = x_account_token
        self._remote_company_id = remote_company_id

    def get_companies(self, modified_after: Optional[datetime] = None) -> dict:
        company_params = {"x_account_token": self._x_account_token}
        if modified_after:
            company_params |= {"modified_after": modified_after}
        try:
            api_response = company_info_api.CompanyInfoApi(
                self._accounting_client
            ).company_info_list(**company_params)
        except ApiException as e:
            raise ApiException(
                f"Exception when calling CompanyInfoApi->company_info_list: {e}\n"
            )
        return api_response

    def get_accounts(
        self, modified_after: Optional[datetime] = None, cursor: Optional[str] = None
    ) -> dict:
        """
        TODO: doc
        """
        accounts_params = {"x_account_token": self._x_account_token}
        if modified_after:
            accounts_params |= {"modified_after": modified_after}
        if cursor:
            accounts_params |= {"cursor": cursor}
        try:
            api_response = accounts_api.AccountsApi(
                self._accounting_client
            ).accounts_list(**accounts_params)
        except ApiException as e:
            api_response = {
                "error": f"Exception when calling AccountsApi->accounts_list: {e}\n"
            }
        return api_response

    def get_transactions(
        self, modified_after: Optional[datetime] = None, cursor: Optional[str] = None
    ) -> dict:
        accounts_params = {"x_account_token": self._x_account_token}
        if modified_after:
            accounts_params |= {"modified_after": modified_after}
        if cursor:
            accounts_params |= {"cursor": cursor}
        try:
            api_response = expenses_api.ExpensesApi(
                self._accounting_client
            ).expenses_list(**accounts_params)
            api_response_3 = transactions_api.TransactionsApi(
                self._accounting_client
            ).transactions_list(**accounts_params)
            api_response_2 = income_statements_api.IncomeStatementsApi(
                self._accounting_client
            ).income_statements_list(**accounts_params)
        except ApiException as e:
            api_response = {
                "error": f"Exception when calling TransactionsApi->transactions_list: {e}\n"
            }
        print("TRANSACTIONS")
        pprint(api_response_3["results"])
        0 / 0
        return api_response
