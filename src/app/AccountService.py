from fastapi import Depends
from src.adapters.database.Account import SqlAccountRepository
from src.app.Account import (
    Account,
    AccountRepository,
)
from src.app.AccountDto import (
    CreateAccountParams,
    VerifyAccountAndPasswordParams,
)
from src.app.AccountException import (
    InvalidValueError,
    UsernameNotFoundError,
    DuplicatedUsernameError,
)


class AccountService:
    repo: AccountRepository

    def __init__(self, repo: AccountRepository = Depends(SqlAccountRepository)):
        self.repo = repo

    def create_account(self, params: CreateAccountParams):
        account = Account.register(params.username, params.password)
        existingAccount = self.repo.find_account_by_username(params.username)
        if existingAccount is not None:
            raise DuplicatedUsernameError()
        self.repo.create_account(account)

    def login(self, params: VerifyAccountAndPasswordParams):
        account = self.repo.find_account_by_username(params.username)
        if account is None:
            raise UsernameNotFoundError(params.username)

        ok = account.login(params.password)
        self.repo.update_account(account)
        if ok:
            return
        raise InvalidValueError(f"Password does not match. Remaining {account.verified_retry_count} retry attempts.")
