import src.app.Account as Account
from src.app.AccountDto import (
    CreateAccountParams,
    VerifyAccountAndPasswordParams,
)


class AccountService:

    def create_account(self, params: CreateAccountParams):
        Account.Validator.validate(params.username, params.password)

    def verify_account_and_password(self, params: VerifyAccountAndPasswordParams):
        Account.Validator.validate(params.username, params.password)
