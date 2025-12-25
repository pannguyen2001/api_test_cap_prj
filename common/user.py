from .client import Client
from process_responses import RoleProcessResponse, AccountResponse

class User:
    def __init__(
        self,
        role: str = "",
        email: str = "",
        password: str = "",
        *args,
        **kwargs
        ) -> None:
        self.client = Client(role, email, password, *args, **kwargs)
        self.client.login()
        self.AccountResponse = AccountResponse(self.client)
        self.RoleProcessResponse = RoleProcessResponse(self.client)

