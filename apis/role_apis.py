from requests import Response
from typing import Dict
from common.client import Client

class RoleAPI:
    def __init__(self, client: Client = Client()) -> None:
        self.client = client

    def get_all_roles(self) -> Response:
        return self.client.get("/api/roles")

    def get_role_by_id(self, role_id: str = "") -> Response:
        return self.client.get(f"/api/roles/{role_id}")

    def create_role(self, request_body: Dict = None) -> Response:
        return self.client.post("/api/roles", json=request_body)

    def edit_role(self, role_id: str = "", request_body: Dict = None) -> Response:
        return self.client.put(f"/api/roles/{role_id}", json=request_body)

    def delete_role(self, role_id: str = "") -> Response:
        return self.client.delete(f"/api/roles/{role_id}")