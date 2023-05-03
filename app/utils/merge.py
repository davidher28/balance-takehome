from datetime import datetime
from pprint import pprint
from typing import Callable, Iterator, Optional

from app.database.repository import (AccountRepository, CompanyRepository,
                                     SyncStatusRepository,
                                     TransactionRepository)
from app.services.merge import MergeAccounting
from app.settings import settings
from app.utils import BaseUtil


class MergeSyncUtil(BaseUtil):
    def __init__(self):
        super().__init__()
        self.accounting_client = MergeAccounting(
            accounting_auth_key=settings.merge_accounting_auth_key,
            x_account_token=settings.merge_x_account_token,
            remote_company_id=settings.sandbox_company_remote_id,
        )
        sync_status = self.sync_status_repository.get()
        self.last_sync_date = sync_status.last_sync_at if sync_status else None

    @staticmethod
    def data_paginator(request: Callable, params: dict = {}) -> Iterator[dict]:
        """
        Generator function to paginate through Merge API results.
        """
        next_cursor = "next"
        while next_cursor:
            response = request(**params)
            for result in response["results"]:
                yield result
            next_cursor = params["cursor"] = response["next"]

    def company_values_coercer(self, company_values: list[dict]) -> list[dict]:
        return [
            {
                "created_at": company_info["remote_created_at"],
                "modified_at": company_info["modified_at"],
                "legal_name": company_info["legal_name"],
                "name": company_info["name"],
                "remote_id": company_info["id"],
                "tax_number": company_info["tax_number"],
                "fiscal_year_end_day": company_info["fiscal_year_end_day"],
                "fiscal_year_end_month": company_info["fiscal_year_end_month"],
                "currency": company_info["currency"],
            }
            for company_info in company_values
        ]

    def account_values_coercer(self, account_values: list[dict]) -> list[dict]:
        return [
            {
                "created_at": datetime.now(),
                "modified_at": account_info["modified_at"],
                "name": account_info["name"],
                "remote_id": account_info["id"],
                "account_type": account_info["type"],
                "classification": account_info["classification"],
                "status": account_info["status"],
                "current_balance": account_info["current_balance"],
                "currency": account_info["currency"],
                "company_id": settings.sandbox_company_remote_id,
            }
            for account_info in account_values
        ]

    def transaction_values_coercer(self, transaction_values: list[dict]) -> list[dict]:
        return [
            {
                "created_at": datetime.now(),
                "modified_at": transaction_info["modified_at"],
                "name": transaction_info["name"],
                "remote_id": transaction_info["id"],
                "transaction_date": transaction_info["transaction_date"],
                "transaction_to": transaction_info["contact"],
                "transaction_from": transaction_info["status"],
                "amount": transaction_info["total_amount"],
                "currency": transaction_info["currency"],
                "account_id": transaction_info["account"],
                "company_id": settings.sandbox_company_remote_id,
            }
            for transaction_info in transaction_values
        ]

    def sync_companies(self) -> None:
        """
        Companies Polling Process
        """
        newest_companies = self.accounting_client.get_companies(
            modified_after=self.last_sync_date
        )
        coerced_values = self.company_values_coercer(
            company_values=newest_companies["results"]
        )
        self.company_repository.add_batch(coerced_values)

    def sync_accounts(self) -> None:
        """
        Accounts Polling Process
        """
        params = {"request": self.accounting_client.get_accounts}
        if self.last_sync_date:
            params |= {"params": {"modified_after": self.last_sync_date}}
        newest_accounts = list(self.data_paginator(**params))
        coerced_values = self.account_values_coercer(account_values=newest_accounts)
        self.account_repository.add_batch(coerced_values)

    def sync_transactions(self) -> None:
        params = {"request": self.accounting_client.get_transactions}
        if self.last_sync_date:
            params |= {"params": {"modified_after": self.last_sync_date}}
        newest_transactions = list(self.data_paginator(**params))
        coerced_values = self.transaction_values_coercer(
            account_values=newest_transactions
        )
        self.transaction_repository.add_batch(coerced_values)
