from requests import Response
from typing import Dict
from common.client import Client

class AccountAPI:
    def __init__(self, client: Client = Client()) -> None:
        self.client = client

    def get_all_accounts(self) -> Response:
        return self.client.get("/api/accounts")

    def get_account_by_id(self, account_id: int) -> Response:
        return self.client.get(f"/api/accounts/{account_id}")

    def create_account(self, request_body: Dict = None) -> Response:
        return self.client.post("/api/auth/register", json=request_body)

    def edit_account(self, account_id: str = "", request_body: Dict = None) -> Response:
        return self.client.put(f"/api/accounts/{account_id}", json=request_body)

    def delete_account(self, account_id: str = "") -> Response:
        return self.client.delete(f"/api/accounts/{account_id}")
