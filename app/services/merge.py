from datetime import datetime
from typing import Optional, Union

from MergeAccountingClient import ApiClient, ApiException, Configuration
from MergeAccountingClient.api import accounts_api, company_info_api, transactions_api


class MergeAccounting:
    """
    Service Class that allows communication with merge.dev and the synced data, using the MergeAccountingClient SDK.
    """

    def __init__(
        self, accounting_auth_key: str, x_account_token: str, remote_company_id: str
    ):
        config = Configuration()
        config.api_key_prefix["tokenAuth"] = "Bearer"
        config.api_key["tokenAuth"] = accounting_auth_key
        self._accounting_client = ApiClient(config)
        self._x_account_token = x_account_token
        self._remote_company_id = remote_company_id

    def build_query_params(
        self, modified_after: Optional[datetime] = None, cursor: Optional[str] = None
    ) -> dict:
        params: dict[str, Union[str, datetime]] = {
            "x_account_token": self._x_account_token
        }
        if modified_after:
            params |= {"modified_after": modified_after}
        if cursor:
            params |= {"cursor": cursor}
        return params

    def get_companies(self, modified_after: Optional[datetime] = None) -> dict:
        """
        Companies retrieval service using the CompanyInfoApi implementation from merge.dev
        """
        company_params = self.build_query_params(modified_after=modified_after)
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
        Accounts retrieval service using the AccountsApi implementation from merge.dev
        """
        accounts_params = self.build_query_params(
            modified_after=modified_after, cursor=cursor
        )
        try:
            api_response = accounts_api.AccountsApi(
                self._accounting_client
            ).accounts_list(**accounts_params)
        except ApiException as e:
            raise ApiException(
                f"Exception when calling AccountsApi->accounts_list: {e}\n"
            )
        return api_response

    def get_transactions(
        self, modified_after: Optional[datetime] = None, cursor: Optional[str] = None
    ) -> dict:
        """
        Transactions retrieval service using the TransactionsApi implementation from merge.dev
        """
        transactions_params = self.build_query_params(
            modified_after=modified_after, cursor=cursor
        )
        try:
            api_response = transactions_api.TransactionsApi(
                self._accounting_client
            ).transactions_list(**transactions_params)
        except ApiException as e:
            raise ApiException(
                f"Exception when calling TransactionsApi->transactions_list: {e}\n"
            )
        return api_response
